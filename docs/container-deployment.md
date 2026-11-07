# 容器部署交接

## 当前验证状态

- 用户已验证本地留言增删查、后端重启后数据保留、前端 pnpm build。
- Dockerfile、Compose、Nginx、数据库初始化 SQL 均由助手编写，不是框架生成。
- 当前助手环境未找到 Docker 命令。尚未执行 Compose 校验、镜像构建、Nginx 配置校验或容器联调，不能将本地业务通过等同于部署通过。
- 助手未连接云服务器。下面是待用户执行的部署步骤。

## 三个服务

浏览器 → frontend（Nginx，主机 80 端口）→ backend:8000 → db:5432。
只有 frontend 发布主机端口；数据库和后端通过 Compose 内部网络通信。
容器里的 localhost 指容器本身，因此后端使用 DB_HOST=db。
数据库是新建的独立环境，不会自动导入本机测试留言。

数据库初始化 SQL 创建非超级用户 message_board 及同名数据库。
postgres 管理员与应用账户使用不同密码。Alembic 随后创建业务表。
PostgreSQL 18 的数据卷挂载点为 /var/lib/postgresql。

## 1. 准备源码和配置（待执行）

先完成 GitHub 源码提交/推送，再由用户将完整项目放入目标机器的部署目录。
包括两个锁文件、迁移目录与 deploy/postgres/init.sql；不要上传本地 .env、.venv、node_modules。
目标机器需已安装 Docker Engine 和 Compose。以下命令都在含 compose.yaml 的项目根目录执行。

Linux 首次创建配置：

```bash
cp .env.example .env
chmod 600 .env
```

编辑根目录 .env，填写两个不同的部署密码。已有 .env 不要覆盖。
示例中的单引号让 $ 等字符按字面值处理；不要把示例密码用于部署。
backend/.env 只用于本机开发，Compose 不会读取或复制它。
若在 Windows 本地测试，首次复制使用 Copy-Item .env.example .env，可将 HTTP_PORT 改为 8080。

## 2. 校验、构建（待执行）

```bash
sudo docker compose config --quiet
sudo docker compose build
```

--quiet 校验配置但不输出展开后的密码。任一步失败先处理报错，不继续启动。
构建需要下载基础镜像、npm/PyPI 依赖，hello-world 成功不代表这些源均可访问。
在 Windows Docker Desktop 中执行时去掉 sudo。

## 3. 数据库与迁移（待执行）

```bash
sudo docker compose up -d --wait db
sudo docker compose run --rm backend alembic upgrade head
sudo docker compose run --rm backend alembic current
```

预期迁移版本为 0001 (head)。run 创建一次性后端容器执行命令，退出后 --rm 删除该容器，数据卷保留。
init.sql 只在空数据卷首次初始化时执行；后续修改 .env 不会自动修改已有数据库账户密码。

## 4. 启动与验收（待执行）

```bash
sudo docker compose up -d --wait
sudo docker compose exec frontend nginx -t
sudo docker compose ps
curl --fail http://127.0.0.1/api/health
```

若 HTTP_PORT 不为 80，curl 地址需带相应端口。预期 health 返回 status=ok、database=ok。
再从浏览器访问服务器 IP（或本地测试地址），验证页面加载、留言发布、刷新保留、删除。
失败时查看 sudo docker compose logs --tail=100 frontend backend db，分享前去除可能含有的敏感信息。

创建一条验证留言后执行 sudo docker compose restart，再检查留言仍存在。
后续容器重建、服务器重启、备份恢复、更新和回滚需分别验收，不算作本轮已完成。
单独重建 backend 后，应重启 frontend，让 Nginx 重新解析后端容器地址。

## 数据与版本说明

- 常规停止可用 docker compose stop；docker compose down 默认保留命名卷。
- 不在常规更新中使用 down -v：它会删除数据库数据卷。
- 持久化卷不等于备份；首次真实数据更新前另行完成备份及恢复验证。
- 基础镜像使用可更新的系列标签，尚未固定 digest；依赖使用锁文件，uv/pnpm 工具版本固定。
- 本次不包含自动发布或自动回滚。应用代码回滚与数据库回退分开处理，不能盲目执行迁移降级。

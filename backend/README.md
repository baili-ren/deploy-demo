# 留言板后端

## 当前步骤：验证留言业务闭环

当前入口已挂载数据库健康检查和留言增删查路由。用户已确认依赖安装与 0001 迁移成功。
在 backend 目录执行：

```powershell
uv run uvicorn backend.main:app --reload
```

打开 http://127.0.0.1:8000/api/health，预期返回 {"status":"ok","database":"ok"}。
http://127.0.0.1:8000/docs 提供接口文档。此次健康检查会实际查询数据库。

以下步骤供新环境复现使用；当前本地无需重复创建账户或数据库。前端增删查与重启持久化待用户验证。

Python 3.13、uv、FastAPI、SQLAlchemy 2 同步 ORM、psycopg 3、Alembic。
使用 src 包布局。路由在 routes.py，数据库模型在 models.py，输入输出模型在 schemas.py，
连接和每请求 Session 在 db.py，环境配置在 config.py。

以下命令均由用户在本地执行。

## 1. 安装依赖

在 backend 目录运行：

```powershell
uv sync --locked
```

从现有项目恢复环境使用 uv sync --locked，按锁文件安装依赖；新增依赖时使用 uv add 包名。不要手动编辑锁文件。

## 2. 创建本地数据库

使用本机已有的 PostgreSQL 管理账户连接（下面假设账户 postgres、端口 5432）：

```powershell
psql -h 127.0.0.1 -p 5432 -U postgres -d postgres
```

在 psql 内逐条执行；如果已有同名角色或数据库，先检查再复用，不删除已有数据：

```sql
CREATE ROLE message_board LOGIN;
\password message_board
CREATE DATABASE message_board OWNER message_board;
\q
```

\password 会交互式提示输入新角色密码，不需要在 SQL 历史中写明文密码。

## 3. 配置、迁移、启动

首次配置时复制示例（已有 .env 则直接编辑，不覆盖）：

```powershell
Copy-Item .env.example .env
```

编辑 .env，将 DB_PASSWORD 改为上一步角色密码；必要时调整主机、端口。
含 # 或空格的密码用双引号包围。不要提交 .env 或分享密码。

```powershell
uv run alembic upgrade head
uv run alembic current
uv run uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

迁移创建表；服务不会在启动时隐式建表。current 应显示 0001 (head)。
命令必须在 backend 目录执行，以加载该目录的 .env。

## 4. 验证最小闭环

- 打开 http://127.0.0.1:8000/api/health，预期 status 和 database 均为 ok。
- 打开 http://127.0.0.1:8000/docs，可单独操作查询、新增、删除接口。
- 另开终端进入 frontend，运行 pnpm dev。开发代理保留 /api 前缀并转发至 8000。
- 前端发布留言、刷新页面确认存在；停止并重新启动后端后确认仍存在；删除并刷新确认消失。
- 通过 /docs 提交仅含空白的内容应返回 422，删除不存在的 ID 应返回 404。
- 前端构建：在 frontend 运行 pnpm build；后端静态语法检查不等于业务验证。

当前接口不含登录，列表不分页，适用于本次小规模学习验证。
本步骤没有连接云服务器；Dockerfile、Compose、Nginx 和线上部署交接后续准备。

# 部署实操记录

更新时间：2026-11-06

## 目标与协作方式

用一个尽量简化、结构清楚、可持续扩展的留言板项目，亲手跑通部署、验证、更新和回滚。

- 用户亲手执行关键部署操作；助手准备代码、配置、命令说明并协助排错。
- 每完成一个阶段或解决一个卡点，由助手更新本记录。
- 仅将实际执行并有结果支持的操作标为完成；计划、假设与已验证事实分开记录。
- 不记录密码、SSH 私钥、API Key 等秘密。

## 当前进度

- 已确认：项目使用 Vue 3 + TypeScript、FastAPI、PostgreSQL。
- 已确认：采用 Docker Compose + Nginx，当前不使用 Kubernetes。
- 已确认：用户选择腾讯云 4 核 4GB 服务器方案。
- 已完成：创建项目目录和本部署记录。
- 已完成：用户在 Codex 左侧项目中添加本地文件夹，并将当前聊天移入项目；已确认当前工作目录为 F:\2026_code\deploy-demo，部署记录读取正常。
- 已确认（用户控制台截图）：腾讯云轻量实例已创建并运行中；上海 / 上海五区，4 核 4GB，40GB SSD，3Mbps，300GB/月流量；到期时间显示 2027-11-05 20:09:36。
- 已确认：实际操作系统 Ubuntu 24.04.4 LTS；Hermes 预装服务运行情况待检查。
- 已完成：通过腾讯云 OrcaTerm 控制台免密登录，以 ubuntu 用户执行系统、内存和磁盘检查（用户终端截图确认）。本地电脑 SSH 密钥连接尚未配置验证。
- 已完成：Docker Engine 与 Compose 安装；用户输出确认客户端、服务端均可响应。
- 已完成：hello-world 镜像下载与测试容器运行验证，阶段一（服务器基础环境准备）完成。
- 尚未执行：项目编写、本地验证、线上部署。
- 当前卡点：暂无已报告的技术故障。
- 已完成：Caddy 停止并取消开机启动，80 端口已验证释放。
- 下一步：阶段二，准备最小 Vue 3 + FastAPI + PostgreSQL 留言板，以及 Dockerfile、Compose 和 Nginx 配置。

## 项目范围

最小留言板：输入留言、提交、展示列表、删除留言。

- 前端：独立 API 请求层，基本加载状态和错误提示。
- 后端：查询、新增、删除留言接口及健康检查；区分路由、数据库访问和配置。
- 数据库：一张留言表，包含 ID、内容、创建时间；使用初始数据库迁移。
- 暂不加入登录、权限、Redis、Agent 或本地大模型。
- 后续 Agent 功能可通过后端调用模型 API，密钥仅在服务端配置。

## 部署结构

浏览器 → 服务器 IP:80 → Nginx

- 页面请求：返回 Vue 构建的静态文件。
- /api/ 请求：转发到 FastAPI，由后端访问 PostgreSQL。
- Compose 管理前端/Nginx、后端、数据库三个服务。
- 数据库使用持久化卷，不直接暴露到公网；持久化不代替备份。

## 环境信息

| 项目 | 当前记录 |
| --- | --- |
| 本地项目目录 | F:\2026_code\deploy-demo |
| 云厂商 | 腾讯云 |
| 实际配置 | 4 核 4GB（控制台截图确认） |
| 产品类型 | 腾讯云轻量应用服务器，特惠型实例 |
| 地域、磁盘、带宽、流量额度 | 上海 / 上海五区；40GB SSD；3Mbps；300GB/月 |
| 服务器操作系统与预装应用 | Ubuntu 24.04.4 LTS；Hermes 运行状态待检查 |
| 服务器部署目录 | 待确定 |
| 域名与 HTTPS | 后续安排；当前先验证 IP 访问 |

## 实施步骤与验收

以下为整体路线；服务器基础准备（步骤 1、3 的基础环境部分）已完成，具体证据见下方记录。项目准备、发布及后续验收尚未完成。

1. 确认服务器：SSH 登录，查看系统、资源及已有服务；如预装 Hermes，先检查其资源和端口占用再决定是否停止。
2. 准备项目：编写代码、Dockerfile、Compose、Nginx 配置与环境变量示例；本地验证留言增删查。
3. 准备服务器：安装 Docker / Compose，配置必要访问端口和部署目录。
4. 首次发布：上传源码，在服务器构建镜像，执行数据库迁移并启动；通过公网 IP 验证留言增删查。
5. 验证运行：查看日志，退出 SSH、重启服务、重建容器及重启服务器后检查恢复与数据保留。
6. 更新与回滚：发布一次小改动，再切回旧版本；代码回滚与数据库变更分别处理。
7. 后续自动化：手动流程稳定后，再接入镜像仓库和 CI/CD。

首次发布路线：本地源码 → 上传服务器 → 构建 Docker 镜像 → 数据库迁移 → Compose 启动。

前端构建时生成静态文件，由 Nginx 提供服务；后端镜像包含代码与 Python 依赖；数据库使用官方镜像。

## 已验证的操作步骤

### 2026-11-05：首次服务器检查（用户执行，截图验证）

- 入口：腾讯云 OrcaTerm 控制台免密登录。
- whoami：ubuntu。
- cat /etc/os-release：Ubuntu 24.04.4 LTS。
- free -h：内存总量 3.6Gi，已用 871Mi，可用 2.8Gi；Swap 总量 1.9Gi，已用 0B。此为检查时快照。
- df -h /：根分区 /dev/vda2，40G，已用 13G，可用 26G，使用率 34%。
- 以上均为只读检查；尚未安装软件或部署项目。

后续每条记录包含：执行位置、命令、作用、实际结果、验证方法。未执行的命令标注为待执行。

## 问题与解决

暂无实际故障记录。后续记录现象、确认原因、处理方法及验证结果；未确认原因标为假设。

## 操作注意事项

- 明确区分删除容器、删除镜像和删除数据库数据；不把清空数据当作常规更新步骤。
- 不将密钥写入前端、源码仓库或本记录。
- 大陆节点公开建站前，按云厂商要求确认备案事项。
- 日志或命令输出共享前去除秘密信息。




### 2026-11-05：Docker 与端口检查（用户执行，截图验证）

- docker --version 与 docker compose version 均返回 docker 命令未找到；尚未安装或验证 Docker / Compose。
- sudo ss -lntp 显示：sshd 监听 22；Caddy 监听 *:80 和 127.0.0.1:2019；systemd-resolved 监听本地 53。
- 80 端口已被 Caddy 占用，不能直接让新 Nginx 同时绑定该端口。
- Caddy 可能由 Hermes 镜像预装，但用途尚未确认；需要查看服务及配置，不能将此推测当作事实。
- 截图底部有安装命令建议，未看到执行结果，不记为已安装。

### 2026-11-05：确认 Caddy 配置（用户终端输出验证）

- caddy.service 为 active (running)，且 enabled（开机启动）。
- 启动配置为 /etc/caddy/Caddyfile；当前 :80 站点仅启用 root * /usr/share/caddy 和 file_server。
- reverse_proxy 和 php_fastcgi 均为注释，当前配置没有启用反向代理；静态目录具体内容尚未检查。
- 计划由用户执行 sudo systemctl disable --now caddy，再检查服务状态和 80 端口；尚未收到执行结果，不能记为已停止。
- 此操作会停止现有静态站点，但保留软件、配置和文件；可用 sudo systemctl enable --now caddy 恢复（恢复前需确认 80 端口未被新服务占用）。

### 2026-11-06：APT 安装遇到下载问题

- 用户已验证 Caddy 为 inactive / disabled，80 端口无监听；停止和取消开机启动已完成。
- 协作调整：用户自行阅读官方教程并执行，助手解释选择和实际报错，避免逐条复制命令式教学。
- 选用 Docker 官方 APT 仓库安装 Engine 和 Compose 插件。
- 下载官方公钥时 curl 报 Connection reset by peer，docker.asc 未生成；chmod 文件不存在是后续错误。
- apt update 获取 download.docker.com 的 noble/InRelease 时 TLS 握手失败；其他多个源正常响应。
- 判断：当前服务器至 Docker 下载站的连接失败，具体网络原因未确认；不能视为 Docker 安装成功。
- 下一步拟使用清华 Docker CE 软件包镜像修复公钥下载及仓库地址；尚未执行验证。

### 2026-11-06：Docker 安装完成（用户输出验证）

- 用户按更换清华 Docker CE APT 下载源的流程继续安装，并提供版本检查结果。
- sudo docker version：Client 与 Server 均为 Docker Engine Community 29.9.3，linux/amd64；服务端能响应。
- docker compose version：v5.7.0。
- 已确认安装及服务通信成功；镜像拉取、容器实际运行尚未验证。
- 下一步命令（待用户执行）：sudo docker run --rm hello-world。

### 2026-11-06：测试镜像拉取超时

- 用户执行 sudo docker pull hello-world，连接 registry-1.docker.io:443 超时（i/o timeout），未完成镜像下载或容器运行验证。
- 不是 Docker 安装失败；当前故障发生在访问 Docker Hub，确切网络/DNS 原因尚未确认。
- 下一步：按腾讯云轻量官方文档，在 /etc/docker/daemon.json 配置 registry-mirrors 为 https://mirror.ccs.tencentyun.com，保留已有配置；重启 Docker 后重试。此为计划，尚未执行验证。
- 参考：https://cloud.tencent.cn/document/product/1207/45596

### 2026-11-06：阶段一验收通过

- 用户已验证 Docker 加载腾讯云 registry-mirrors 配置；curl 检查镜像服务 /v2/ 返回 HTTP/2 200，证书验证通过。
- 用户执行 sudo docker run --rm hello-world，输出 Hello from Docker!，证明客户端与服务端通信、测试镜像获取和容器执行链路成功。
- --rm 会删除退出后的测试容器，下载的镜像保留。
- 阶段一完成；后续项目所需各镜像的可下载性仍需在实际构建部署时验证。
- 后续主线：准备最小项目 → 上传构建并部署 → 验证持久化、更新和回滚。暂不加入本地 SSH、域名、Kubernetes 等额外任务。

### 2026-11-06：阶段二开始——本地工具检查

- 执行位置：本地 PowerShell，F:\2026_code\deploy-demo；助手执行只读版本检查。
- 已验证：`node --version` 返回 `v22.18.0`；`pnpm --version` 返回 `12.6.0`。
- 已验证：项目根目录当前仅有 docs 目录，尚无前端或后端脚手架。
- 已查阅 Vue 官方快速开始：https://vuejs.org/guide/quick-start.html；当前文档的 Node 要求为 `^22.18.0 || >=24.12.0`，本机版本满足。
- 协作约定：用户操作脚手架、依赖安装与关键命令；助手解释选项，后续补充最小业务代码和部署配置。本阶段不操作云服务器。
- 下一步（待用户执行）：在项目根目录运行 `pnpm create vue@latest`，项目名为 `frontend`，启用 TypeScript；其余可选功能暂不启用，如询问是否跳过示例代码则选择是。
- 后续计划：前端脚手架 → 最小 FastAPI 与 PostgreSQL 业务及初始迁移 → Dockerfile / Compose / Nginx → 构建和业务验证 → 部署交接。每个小阶段分别记录实际结果。
- 构建验证：尚未执行；版本检查成功不代表依赖安装、前端构建或容器构建成功。
- 当前交接点：等待用户完成前端脚手架并提供终端结果；尚未生成业务代码、安装依赖或连接服务器。

### 2026-11-06：阶段二——前端脚手架与最小页面

- 用户反馈前端初始化完成、运行无明显问题；尚未提供浏览器截图或构建输出。
- 助手检查文件确认：frontend 为 Vue 3 + Vite + TypeScript 项目，存在 node_modules 和 pnpm-lock.yaml；不能仅凭目录存在认定安装或构建完全成功。
- 已编写：src/App.vue 留言输入、列表、删除确认、加载及错误提示；src/api/messages.ts 独立请求层，10 秒超时；src/style.css 简单响应式样式。
- 已配置：Vite 开发代理将 /api 转发到 http://127.0.0.1:8000，保留 /api 前缀。此代理仅用于开发，生产环境后续由 Nginx 提供。
- 已添加：根目录 .gitignore，排除依赖、构建产物、Python 虚拟环境与 .env 等秘密配置，保留 .env.example。
- 接口约定（后端待实现）：GET /api/messages 返回数组，按新到旧排序；POST /api/messages 接收 {content} 并返回新留言；DELETE /api/messages/{id} 成功返回 204。留言字段为 id、content、created_at（含时区的 ISO 时间）；内容去除首尾空白后长度 1–1000。
- 当前没有后端或数据库，不能验收真实留言增删查；页面请求失败属于当前未接通后端的状态，没有使用假数据冒充持久化。
- 构建验证：待用户在 frontend 执行 pnpm build（vue-tsc -b && vite build），本轮未代执行。浏览器效果亦待用户验证。
- 交接：用户重启 pnpm dev 查看新页面，并执行 pnpm build 提供结果；构建通过后准备 FastAPI、PostgreSQL 和初始迁移，再补 Docker Compose / Nginx。GitHub 上传、镜像构建、云端部署均未执行；本轮未操作服务器。

### 2026-11-06：后端准备——uv 安装验证

- 用户执行 uv --version，返回 uv 0.13.7 (316c827e0 2026-11-03 x86_64-pc-windows-msvc)，确认本地 uv 可用。
- 后端由用户按步骤创建；助手解释命令并在后续补充代码。采用 uv 管理项目环境和依赖。
- 下一步（待用户执行）：在项目根目录运行 uv init backend --python 3.13 --vcs none，进入 backend 后运行 uv sync，再用 uv run python --version 验证项目解释器。
- Python 3.13 为本项目选定版本；尚未验证本地是否已安装，uv 可能需要下载。--vcs none 避免在 backend 内单独初始化 Git 仓库，后续统一管理项目根目录。
- 后端初始化、依赖安装、FastAPI 启动、前端构建均未收到成功输出，仍为待验证。

### 2026-11-06：阶段二——最小后端代码准备

- 用户确认本地已有 PostgreSQL。助手发现 psql 位于 D:\PostGreSQL\bin\psql.exe；服务状态查询因权限不足失败，未提权、未确认数据库可连接。
- 文件检查确认 backend 使用 src/backend 包布局、Python 3.13 声明、uv 构建后端，存在 .venv 和 uv.lock；依赖列表目前为空。
- 已编写：FastAPI 入口和路由、Pydantic 输入输出模型、pydantic-settings 配置、SQLAlchemy 2 同步 ORM 与每请求 Session、psycopg 连接配置、Alembic 初始迁移、.env.example 和 README 操作步骤。
- 接口：GET /api/health 检查数据库连接；GET/POST /api/messages；DELETE /api/messages/{message_id}。新增返回 201，删除成功 204，不存在 404，非法内容由 Pydantic 返回 422。
- 已验证：使用 backend/.venv/Scripts/python.exe 对 9 个 Python 文件执行 ast.parse，全部语法通过。此检查不导入第三方依赖，不证明 API 可启动或业务通过。
- 待用户执行：README 中的 uv add 命令（更新 pyproject.toml 与 uv.lock）→ 创建本地数据库和角色 → 配置 .env → uv run alembic upgrade head → 启动 Uvicorn → 前端真实增删查与后端重启持久化验证。
- 构建及联调结果：前端 pnpm build 尚无输出；后端依赖安装、迁移、服务启动、数据库读写均待验证。尚未进行容器构建、GitHub 上传或云服务器操作。
- 交接入口：backend/README.md；后续验证通过再准备 Dockerfile、Compose 和 Nginx，阶段二尚未完成。

### 2026-11-06：PyCharm 终端无法识别 uv——已解决

- 用户确认 Windows 用户 Path 已包含 C:\Users\dell\.local\bin，uv.exe 实际位于该目录。
- 用户手动完全关闭并重新打开 PyCharm 后，终端可正常使用 uv；无需重复安装或修改永久环境变量。
- 现象与旧 IDE 进程未继承更新后的环境变量一致；没有进一步检查进程继承链。
- 协作调整：逐步安装和验证，先 FastAPI + Uvicorn，再接数据库；优先持久、常规的配置方式，不把临时修改终端 PATH 作为默认解决方案。
- 下一步待用户执行：在 backend 运行 uv add fastapi uvicorn；若之前已成功执行则无需重复。之后调整入口为不依赖数据库的最小接口并启动验证。现有数据库代码保留，但依赖安装和业务联调仍待验证。

### 2026-11-06：最小 FastAPI 入口准备完成

- 已检查 pyproject.toml 声明 fastapi>=0.162.0、uvicorn>=0.54.0；用项目 .venv 的 Python 成功导入应用，确认实际安装版本分别为 0.162.0、0.54.0。
- main.py 已调整为独立 FastAPI 入口，仅提供 GET /api/health 返回 {"status":"ok"}；数据库路由暂未挂载，数据库代码保留供后续接入。
- 已验证：应用导入成功，路由表包含 /api/health 和自动文档路由。未启动 HTTP 服务，不能记为浏览器访问成功。
- 待用户执行（backend 目录）：uv run uvicorn backend.main:app --reload；打开 http://127.0.0.1:8000/api/health 验证返回值，并可查看 /docs。
- 当前健康检查仅验证 HTTP 服务，不验证 PostgreSQL；前端留言增删查、迁移、生产构建和部署均仍待执行验证。

### 2026-11-06：FastAPI HTTP 验证通过，PyCharm 运行配置待修正

- 用户确认通过 uv run uvicorn 启动后，页面效果符合预期；当前浏览器上下文为 http://127.0.0.1:8000/docs。记为用户验证通过，非助手直接请求验证。
- 用户使用 PyCharm 直接运行 main.py 时，日志显示解释器为 uv 管理的全局 CPython 3.12.14，而非 backend/.venv，报 ModuleNotFoundError: No module named 'fastapi'。
- 待修正：PyCharm 项目及运行配置选择 F:\2026_code\deploy-demo\backend\.venv\Scripts\python.exe；以模块 uvicorn 启动，参数 backend.main:app --reload，工作目录 backend。
- 即使解释器修正，直接执行仅定义 app 的 main.py 也不会启动 HTTP 服务；应使用 Uvicorn 运行配置。无需给另一套全局 Python 重复安装依赖。

### 2026-11-06：本地 PostgreSQL 连接验证通过

- 用户截图确认通过 psql 连接 127.0.0.1:5432，使用 postgres 账户登录，出现 postgres=# 提示符。
- 截图显示 psql 客户端版本 18.6；未查询数据库服务端版本，不将客户端版本视为服务端版本。
- 下一步待用户在 psql 创建 message_board 登录角色、交互设置密码并创建同名数据库，随后验证专用账户连接。尚未创建业务表或验证留言持久化。

### 2026-11-07：专用数据库连接验证通过

- 用户确认专用账户连接后的查询结果符合预期：current_user=message_board、current_database=message_board、current_schema=public。属于用户验证结果。
- 助手检查确认后端目前仅声明 FastAPI 与 Uvicorn；数据库相关依赖尚未声明。
- 已从 .env.example 创建缺失的 backend/.env，仅含示例占位密码，待用户本地填写；不记录或输出真实密码。
- 下一步待用户执行：安装 sqlalchemy、psycopg[binary]、pydantic-settings，填写 .env。数据库迁移工具随后安装，当前不挂载业务路由，HTTP 健康检查仍不检查数据库。
- 数据库表创建、后端数据库连接、留言业务与构建仍待验证。

### 2026-11-07：数据库依赖与配置准备完成，迁移待执行

- 用户确认依赖安装和 .env 填写完成；助手检查 pyproject.toml 已声明 sqlalchemy、psycopg[binary]、pydantic-settings。
- 助手通过项目 Python 加载 backend.db 并尝试只读连接，连接 127.0.0.1:5432 被系统拒绝，错误 Permission denied (10013)。未读取或输出密码；此结果不是认证失败，也不能证明用户终端无法连接。未提权。
- 下一步由用户在 backend 执行 uv add alembic，再执行 uv run alembic upgrade head 和 uv run alembic current。
- upgrade head 将使用 .env 连接数据库并执行已有初始迁移；预期创建 public.messages 和 Alembic 版本记录表。尚未执行，不能记为连接或建表成功。

### 2026-11-07：迁移验收通过，留言路由已挂载

- 用户确认迁移执行结果符合预期：alembic current 显示 0001 (head)。属于用户验证结果；助手未直接查询表。
- 已将 main.py 改为挂载 routes.router，移除临时健康检查。/api/health 现在实际检查数据库连接；留言 GET/POST/DELETE 接口已注册。
- 已验证：项目 Python 成功导入应用并生成 OpenAPI，包含健康检查与留言查询、新增、删除。此检查未连接数据库，不代表增删查通过。
- README 已更新当前状态，移除过时的依赖上限安装示例，新环境采用 uv sync --locked 恢复依赖。
- 待用户验收：刷新 /docs 和 /api/health → 前端发布一条留言 → 刷新仍存在 → 重启后端仍存在 → 删除并刷新确认消失。若服务未自动重载，由用户重启。
- 前端构建、业务闭环、容器构建和线上部署仍未验收；未操作云服务器。

### 2026-11-07：本地留言最小闭环验收通过（用户验证）

- 用户确认此前整套验收结果符合预期：数据库健康检查、前端发布留言、页面刷新保留、后端重启后保留、删除并刷新消失。
- 用户截图确认：pgAdmin 以 postgres 连接 message_board（超级用户）；psql 以 postgres 连接 postgres（超级用户）；PyCharm DB Browser 以 message_board 连接 message_board（非超级用户）。
- PyCharm 截图可见 public.messages 与 public.alembic_version 两张表，支持迁移已建表的记录。
- 本地业务闭环完成，以上为用户反馈和截图证据，不表述为助手独立执行的端到端测试。
- 下一步待用户在 frontend 执行 pnpm build，验证 TypeScript 检查与生产静态资源构建；随后准备并讲解 Dockerfile、Compose 和 Nginx。生产构建、容器构建、GitHub 上传、线上部署尚未验收。

### 2026-11-07：前端生产构建通过，前端容器配置已准备

- 用户确认 pnpm build 结果符合预期，记为本地 TypeScript 检查与 Vite 生产构建通过（用户验证，未提供构建耗时与产物大小）。
- 助手编写 frontend/Dockerfile：Node 22 构建阶段使用 pnpm 12.6.0 和冻结锁文件安装，执行 pnpm build；最终镜像使用 Nginx 提供 dist 静态资源。
- 助手编写 frontend/.dockerignore，避免复制本机依赖、构建产物和 .env 等配置到构建上下文。
- 助手编写 frontend/nginx.conf：页面请求返回静态文件，/api/ 保留前缀转发至 backend:8000。backend 是后续 Compose 服务名，不是本机地址；需要 Compose 网络和后端服务，不应单独启动该 Nginx 容器验证业务。
- 本次配置为助手手写，非脚手架生成。尚未执行 Docker 镜像构建或 nginx -t；基础镜像及 npm 包在构建环境的下载能力待验证。镜像标签使用可更新的版本系列，未固定 digest。
- 后续交接：补充后端 Dockerfile、Compose、部署环境变量示例及迁移顺序，再由用户执行构建与启动。当前未操作云服务器。

### 2026-11-07：部署配置准备完成，容器验证待执行

- 新增 backend/Dockerfile、backend/.dockerignore、compose.yaml、根目录 .env.example、deploy/postgres/init.sql 和 docs/container-deployment.md，均由助手手写。
- 后端镜像使用 Python 3.13、uv 0.13.7，按 uv.lock 安装，非 root 用户运行 Uvicorn，生产不启用 --reload。
- Compose 管理 frontend、backend、db 三个服务，只发布 Nginx 的 HTTP 端口。PostgreSQL 18 使用 /var/lib/postgresql 命名卷；首次初始化创建普通应用账户与数据库，管理员密码和应用密码分开。
- 数据库健康检查使用 TCP，避免把初始化时仅开放 Unix socket 的临时服务视为启动完成。应用等数据库健康，Nginx 等后端健康。
- 部署顺序：配置根目录 .env → config --quiet → build → 启动 db 并等待健康 → run --rm backend alembic upgrade head → 启动全部服务 → nginx -t、HTTP 与持久化验收。
- 已验证：引用文件存在，pyproject.toml 和 uv.lock 可解析。没有 Docker 命令，尚未执行 Compose 语法校验、镜像构建、Nginx 校验或容器运行。不能把文件检查当成容器构建通过。
- 构建结果：前端本地生产构建由用户确认通过；Docker 构建待执行。云服务器未操作。
- 部署交接说明：docs/container-deployment.md，包含账户初始化与迁移区别、命名卷、网络、配置、首次发布命令、验收与停止注意事项。GitHub 上传仍待执行，建议部署前完成。阶段二配置已准备，容器验收仍未完成。

### 2026-11-07：Git 忽略规则按目录维护

- 按用户偏好新增 backend/.gitignore，覆盖 Python 环境、缓存、构建产物、秘密配置和编辑器文件；frontend/.gitignore 补齐 .env 忽略与示例保留规则，便于未来独立使用。
- 根目录 .gitignore 保留通用本地配置、日志、编辑器和系统文件规则；技术栈规则分别归前后端目录。少量公共规则在子目录重复是为了支持独立拆分。
- 已用 git check-ignore 验证 .idea、后端 .env/.venv/__pycache__、前端 .env/node_modules/dist 均被对应规则忽略；当前暂存列表不包含 .idea。
- 修改尚未重新暂存；由用户执行 git add .、检查暂存列表、提交和关联远程仓库。助手未提交或推送。

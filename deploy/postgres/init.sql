-- 仅在新的数据库数据卷首次初始化时执行。
-- 从容器环境读取密码，psql 的变量引用会正确转义 SQL 字面量。
\getenv app_password DB_PASSWORD
CREATE ROLE message_board LOGIN PASSWORD :'app_password';
CREATE DATABASE message_board OWNER message_board;

## python3 webapp
```
python3
mysql
aiohttp
```

创建工作目录结构：

```
webapp/            <-- 根目录
|
+- backup/         <-- 备份目录
|
+- conf/           <-- 配置文件
|
+- www/            <-- web目录，存放.py文件
|  |
|  +- static/      <-- 存放静态文件
|  |
|  +- templates/   <-- 存放模板文件
|
+- ios/            <-- 存放ios App工程
|
+- LICENSE         <-- 代码LICENSE
```

### 搭建开发环境

```
$cd webapp
$virtualenv -p /usr/bin/python3 venv
$source venv/bin/activate
(venv)$python --version
Python 3.6.7
(venv)$pip install aiohttp
(venv)$pip install jinja2
(venv)$pip install aiomysql
```

[安装并配置mysql](https://github.com/zhudingsuifeng/platform/mysql.md)

```
$pip install mysql-connector
```

### 链接使用mysql服务器的web数据库

```
```

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
import mysql.connector   # 导入Mysql驱动
conn = mysql.connector.connect(user = 'fly', password  = 'password', database = 'web')
# 链接数据库
# 注意把password设为fly的密码
# connect()链接对象
cursor = conn.cursor()   # 游标对象
cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')     # 创建user表
cursor.execute('insert into user(id, name) values(%s, %s), ['1', 'Michael'])
# 插入一行记录，注意mysql的占位符是%s
conn.commit()   # 提交事务
cursor.close()
conn.close()
# 关闭cursor和connection
```

### pytahon数据库的connection和cursor对象

connection对象支持的方法

```
cursor()   使用该链接创建并返回游标
commit()   提交当前事务
rollback() 回滚当前事务
close()    关闭链接
```

游标对象用于执行查询和获取结果

cursor对象支持的方法：

```
execute(op[,args])    执行一个数据库查询和命令
fetchone()            取结果集的下一行
fetchmany(size)       获取结果集的下几行
fetchall()            获取结果集剩下的所有行
rowcount              最近一次execute返回数据的行数或影响行数
close()               关闭游标对象
```

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

[安装并配置mysql](https://github.com/zhudingsuifeng/platform/blob/master/mysql.md)

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

### 协程

协程，又称微线程。英文名coroutine.

子程序调用是通过栈实现的，一个线程就是执行一个子程序。

协程看上去也是子程序，但执行过程中，在子程序内部可中断，然后转而执行别的子程序，在适当的时候再返回来接着执行。

协程最大的优势就是协程极高的执行效率。

第二大优势就是不需要多线程的锁机制，因为只有一个线程，也不存在同时写变量冲突，在协程中控制共享资源不加锁，只需要判断状态。

python对协程的支持是通过generator实现的。

在generator中，我们不但可以通过for循环来迭代，还可以不断调用next()函数获取由yield语句返回的下一个值。

### asyncio

asyncio是python3.4版本引入的标准库，直接内置了对异步IO的支持。

asyncio的编程模型就是一个消息循环。我们从asyncio模块中直接获取一个EventLoop的引用，然后把需要执行的协程扔到EventLoop中执行，就实现了异步IO。

```
import asyncio

def hello():
    print("hello world")
    # 异步调用asyncio.sleep(1) 
    r = yield from asyncio.sleep(1)
    print("hello again")

# 获取EventLoop
loop = asyncio.get_event_loop()
# 执行coroutine
loop.run_until_complete(hello())
loop.close()
```

用asyncio提供的@asyncio.coroutine可以把一个gennerator标记为coroutine类型，然后在coroutine内部用yield from调用另一个coroutine实现异步操作。

### async/await

为了简化并更好地标识异步IO，从python3.t开始引入了新的语法async和await，可以让coroutine的代码更简洁易读。

1. 把@asyncio.coroutine替换为async

2. 把yield from 替换为await

之前代码：

```
@asyncio.coroutine
def hello():
    print("hello world")
    r = yield from asyncio.sleep(1)
    print("hello again")
```

新版代码：

```
async def hello():
    print("hello world")
    r = await asyncio.sleep(1)
    print("hello again")
```

### aiohttp

asyncio可以实现单线程并发IO操作。如果仅用在客户端，发挥的威力不大。如果把asyncio用在服务器端，例如web服务器，由于http连接就是IO操作，因此和以用单线程+coroutine实现多用户的高并发支持。

asyncio实现了TCP，UDP，SSL等协议，aiohttp则是基于asyncio实现的HTTP框架。

需要安装aiohttp:

```
pip install aiohttp
```

编写一个HTTP服务器，代码如下：

```
import asyncio
from aiohttp import web

async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body=b'<h1>Index</h1>')

async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s </h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'))

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/hello/{name}', hello)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print('server started at http://127.0.0.1:8000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
```

注意aiohttp的初始化函数init()也是一个coroutine, loop.create_server()则利用asyncio创建TCP服务。

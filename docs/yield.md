## python协程

### python中的协程三个阶段：

1. 最初的生成器变形yield/send

2. 引入@asyncio.coroutine和yield from

3. 在python3.5版本中引入async/await关键字

### 生成器变形yield/send

普通函数中如果出现了yield关键字，那么该函数就不再是普通函数，而是一个生成器。

```
def mygen(alist):
    while len(alist) > 0:
        c = randint(0, len(alist)-1)
        yield alist.pop(c)

a = ["aa", "bb", "cc"]
c = mygen(a)
print(c)
```

上面代码中的c就是一个生成器。生成器就是一种迭代器，可以使用for进行迭代。生成器函数最大的特点是可以接受外部传入的一个变量，并根据变量内容计算结果后返回。

这一切都是靠生成器内部的send()函数实现的。

```
def gen():
    value = 0
    while True:
        receive = yield value
        if receive == 'e':
            break
        value = 'got: %s' % receive

g = gen()
print(g.send(None))
print(g.send('hello'))
print(g.send(123456))
print(g.send('e'))
```
其中receive = yiedl value包含了3个步骤：

1. 向函数外抛出(返回)value

2. 暂停(pause),等待next()或send()恢复

3. 赋值receive = MockGetValue().这个MockGetValue()是假想函数，用来接收send()发送进来的值。

以上代码执行流程：

1. 通过g.send(None)或者next(g)启动生成器函数，并执行到第一个yield语句结束的位置。运行receive = yield value语句时，实际程序只执行了前面的1，2两步，程序返回了value值，并暂停(pause),并没有执行第3步给receive赋值。因此yield value会输出初始值0.

这里要特别注意：在启动生成器函数时只能send(None),如果试图输入其他的值都会得到错误提示信息。

2. 通过g.send('hello'),会传入hello,从上次暂停的位置继续执行，那么就是运行第3步，赋值给receive。然后算出value的值，并回到while头部，遇到yield value,程序再次执行1，2两步，程序返回了value值，并暂停(pause).此时yield value会输出"got:hello",并等待send()激活。

3. 通过g.send(123456),会重复第2步，最后输出结果为"got:123456".

4. 当我们g.send('e')时，程序会执行break然后退出循环，最后整个函数执行完毕，所以会得到StopIteration异常。

从上面可以看出，在第一次send(None)启动生成器(执行1->2,通常第一次返回的值没有什么用)之后，对于外部的每一次send(),生成器的实际在循环中的运行顺序是3->1->2,也就是先获取值，然后进行操作，最后返回一个值，在暂停等待唤醒。

从语法上来看，协程和生成器类似，都是定义体中包含yield关键字的函数。

yield在协程中的用法：

1. 在协程中yield通常出现在表达式的右边，例如：datum = yield，可以产出值，也可以不产出，如果yield关键字后面没有表达式，那么生成器产出None.

2. 协程可能从用调用方接受数据，调用方法是通过send(datum)的方式把数据提供给协程使用，而不是next(...)函数，通常调用方会把值推送给协程。

3. 协程可以把控制器让给中心调度程序，从而激活其他的协程。

生成器API中增加了.send(value)方法(生成器的调用方可以使用.send()方法发送数据，发送的数据会成为生成器函数中yield表达式的值)

总体上在协程中把yield看作是控制流程的方式。

```
def simple_coroutine():
    print('-->coroutine started')
    x = yield
    print('-->coroutine received:', x)

my_core = simple_coroutine()

next(my_coro)    # 激活

my_coro.send(24)
```

yield 的右边没有表达式，所以这里默认产出的值是None

刚开始先调用了next()是因为这个时候生成器还没有启动，没有停在yield那里，这个时候是无法通过send()发送数据。

所以当我们通过next()激活协程后，程序就会运行到x = yield, x = yield这个表达式的计算过程是先计算等号右边的内容，然后再进行赋值，所以当激活生成器后，程序会停在yield这里，但是并没有给x赋值。

当我们调用send方法后yield会收到这个值并赋值给x,而当程序运行到协程定义体的末尾时和用生成器的时候一样会抛出StopIteration异常。

关于调用next()函数这一步通常称为“预激(prime)”协程，即让协程向前执行到第一个yield表达式，准备好作为活跃的协程使用。

### yield from

```
def g1():
    yield range(5)

def g2():
    yield from range(5)

it1 = g1()
it2 = g2()
for x in it1:
    print(x)

for x in it2:
    print(x)
```

输出：

```
range(0,5)
0
1
2
3
4
```

这说明yield就是将range这个可迭代对象直接返回。

而yield from 解析了range对象，将其中每一个item返回。

yield from iterable本质上等于for item in iterable: yield item 的缩写版。

强调一下：yield from 后面必须跟iterable对象(可以是生成器，迭代器)

### 预激协程的装饰器

```
from functools import wraps

def coroutine(func):
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer

@coroutine
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count +=1
        average = total/count

coro_avg = averager()
from inspect import getgeneratorstate
print(getgeneratorstate(coro_avg))
print(coro_avg.send(10))
print(coro_avg.send(30))
print(coro_avg.send(5))
```

关于预激，在使用yield from句法调用协程的时候，会自动预激活，这样其实与我们上面定义的coroutine装饰器是不兼容的，在python3.4里面的asyncio.coroutine装饰器不会预激协程，因此兼容yield from.

在生成器gen中使用yield from subgen()时，subgen会获得控制权，把产出的值传给gen的调用方，即调用方可以直接控制subgen，同时,gen会阻塞，等待subgen终止。

yield from的主要功能是打开双向通道，把最外层的调用方法与最内层的子生成器联结起来，这样二者可以直接发送和产出值，还可以直接传入异常。

yield from 重要说明：

1. 子生成器产出的值都直接传给委派生成器的调用方(即客户端代码).

2. 使用send()方法发送给委派生成器的值都直接传给子生成器。

3. 生成器推出时，生成器(或子生成器)中的return expr表达式会发出StopIterarion(expr)抛出异常。

4. yield from表达式的值是子生成器终止时传给StopIteration异常的第一个参数。

### asyncio.coroutine和yield from

yield from在asyncio模块中得以发扬光大。之前都是我们手工切换协程，现在当声明函数为协程后，我们通过事件循环来调度协程。

```
import asyncio,random

@asyncio.coroutine
def smart_fib(n):
    index = 0
    a = 0
    b = 1
    while index < n:
        sleep_secs = random.uniform(0, 0.2)
        yield from asyncio.sleep(sleep_secs)   
        # 通常yield from 后都是接的耗时操作
        print('smart one think {} secs to get {}'.format(sleep_secs, b))
        a, b = b, a + b
        index += 1

@asyncio.coroutine
def stupid_fib(n):
    index = 0
    a = 0
    b = 1
    while index < n:
        sleep_secs = random.uniform(0, 0.4)
        yield from asyncio.sleep(sleep_secs)   
        # 通常yield from 后都是接的耗时操作
        print('stupid one think {} secs to get {}'.format(sleep_secs, b))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [smart_fib(10), stupid_fib(10),]
    loop.run_until_complete(asyncio.wait(tasks))
    print('all fib finished')
    loop.close()
```

yield from 语法可以让我们方便地调用另一个generator.

本例中yield from后面接的asyncio.sleep()是一个coroutine里面也用了(yield from),所以线程不会等待asyncio.sleep(),而是直接中断并执行下一个消息循环。当asyncio.sleep()返回时，线程就可以从yield from拿到返回值(此处为None),然后接着执行下一行语句。

asyncio是一个基于事件循环的实现异步IO的模块。通过yield from,我们可以将协程asyncio.sleep的控制权交给事件循环，然后挂起当前协程；之后，由事件循环决定何时唤醒asyncio.sleep，接着向后执行代码。

协程之间的调度都是由事件循环决定。

yield from asyncio.sleep(sleep_secs)这里不能用time.sleep(1)因为time.sleep()返回的是None,它不是iterable,记得之前说的yield from 后面必须跟iterable对象(可以是生成器，迭代器).

### async和await

python3.5中引入async和await，可以理解为是asyncio.coroutine/yield from 的替代品。

加入新的关键字async，可以将任何一个普通函数变成协程。

```
import time, asyncio, random

async def mygen(alist):
    while len(alist) > 0:
        c = randint(0, len(alist)-1)
        print(alist.pop(c))

a = ["aa", "bb", "cc"]
c = mygen(a)
print(c)
```

输出：

```
<coroutine object mygen at 0x....>
```

但是async对生成器是无效的。async无法将一个生成器转换成协程。

```
async def mygen(alist):
    while len(alist) > 0:
        c = randint(0, len(alist)-1)
        yield (alist.pop(c))

a = ["ss", "dd", "gg"]
c = mygen(a)
print(c)
```

输出：

```
<async_generator object mygen at 0x.....>
```

并不是coroutine协程对象。

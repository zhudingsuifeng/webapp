## python 面试题

- 深拷贝和浅拷贝的区别是什么？

+ 深拷贝事件对象本身复制给另一个对象。这意味着如果对对象的副本进行更改时不会影响原对象。在python中，使用deepcopy()函数进行深拷贝。

+ 浅拷贝时将对象的引用复制给另一个对象。因此，如果我们在副本中进行更改，则会影响原对象。使用copy()函数进行浅拷贝。

- 列表和元组有什么不同？

+ 主要区别在于列表是可变的，元组是不可变的。

```
mylist = [1,2,3]
mytuple = (1,2,3)

mylist[1] = 6
mytuple[1] = 6  # TypeError:'tuple' object does not support item assignment
```

- 解释python中的三元表达式

+ 对应java中的?运算符

```
c = a > b ? 1 : 2
```

+ 当a大于b时，c等于1，否则等于2.

+ python替换方式

```
c = 1 if a > b else 2
```

- python 中如何实现多线程？

+ 线程是轻量级的进程，多线程允许一次执行多个线程。

+ GIL(全局解释器锁)确保依次执行单个线程。一个线程保存GIL并在将其传递给下一个线程之前执行一些操作，这就产生了并行执行的错觉。但实际上，只是线程轮流在CPU上。所有传递都会增加执行的开销。

- 什么是flask?

+ flask是一个使用Python编写的轻量级的web应用框架，使用BSD授权。其WSGI工具箱采用Werkzeug，模板引擎则使用Jinja2。除了Werkzeug和Jinja2以外几乎不依赖任何外部库。因此，flask被称为轻量级框架。

+ flask的回话使用签名cookie来允许用户查看和修改回话内容。他会记录从一个请求到另一个请求的信息。如果要修改会话，则必须有秘钥Flask.secret_key。

- 如何在python中管理内存？

+ Python用一个私有堆内存空间来放置所有对象和数据结构，我们无法访问提。它由解释器来管理。不过使用一些核心API，可以访问一些Python内存管理工具控制内存分配。

- 解释Python中的help()函数和dir()函数。

+ help()函数返回帮助文档和参数说明。

```
help(print)
```

+ dir()函数返回对象中的所有成员(任何类型)

```
dir(print)
``` 

- 当退出python时是否释放所有内存分配？

+ 否，那些具有对象循环引用或者全局命名空间引用的变量，在Python退出时往往不会被释放。

+ 不会释放C库保留的部分内容。

- 什么是猴子补丁？

+ 在运行时动态修改类和模块

+ 属性在运行时的动态替换，叫做猴子补丁(Monkey Patch)。

+ 猴子补丁在带来便利的同时，也有搞乱源代码优雅的风险。

- 给属性打补丁

```
import math

math.pi = 3    # 给标准库打补丁，即运行时修改math的pi属性
```

- 给类方法打补丁

```
class Foo(object):
    def bar(self):
        print('Foo.bar')

def bar(self):    # 补丁
    print('Modified bar')

Foo.bar = bar  # 给Foo的bar方法打补丁，即运行时修改类的方法
```

+ 被修改的类的所有实例中的方法都会被更新，所以更新后的方法不仅仅存在于新创建的对象中，之前创建的所有对象都会拥有更新之后的方法，除非只是新增而不是覆盖掉原来的方法。

+ 修改或者新增的方法应当是与对象绑定的，所以方法的第一个参数应当是被调用的对象。

- 给类实例打补丁

+ 单个对象也可以在不影响这个类的其他实例的情况下打补丁。

```
def herd(self, sheep):
    self.run()
    self.bark()

border_collie = Dog()
border_collie.herd = herd

border_collie.herd(sheep)
# TypeError:herd() takes exactly 2 arguments (1 given)
# The problem with the previous code is that the herd is not a bound method
```

+ 出错的原因就是被调用的对象并没有作为第一个参数传递给我们写的函数。解决这个问题的正确方案是用types这个模块里的MethodType函数

```
import types

border_collie = Dog()
border_collie.herd = types.MethodType(herd, border_collie)

border_collie.herd(sheep)
```

+ 运行中替换或者添加方法是非常有用的，比如说在单元测试中，有些负责和外界服务通信的函数据需要替换掉，方便测试。

- 猴子补丁主要作用

+ 在运行时替换方法、属性等。

+ 在不修改第三方代码的情况下增加原来不支持的功能。

+ 在运行时为内存中的对象增加patch而不是在磁盘的源代码中增加。

+ 猴子补丁的主要作用功能便是在不去改变源码的情况下而对功能进行追加和变更，对于编程过程中使用一些第三方不满足需求的情况下，使用猴子补丁是非常方便的。

- 什么是python字典？

+ 字典是可变的

- 能否解释一下*args和**kwargs？

+ 

- 什么是负索引？

+ 于正索引相反，负索引从右边开始检索。

- 如何随机打乱列表中元素，要求不引用额外的内存空间？

+ 使用random包中的shuffle()函数来实现。

- 解释Python中的join()和split()函数

+ join()函数可以将指定的字符添加到字符串中。

+ split()函数可以用指定的字符分割字符串。

- Python中标识符的命名规则？

+ 只能以下划线或者字母开头。

+ 其余部分能使用字母、下划线或者数字。

+ Python区分大小写。

+ 关键字不能作为标识符。


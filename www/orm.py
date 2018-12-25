#!/home/fly/git/webapp/venv/bin/python
#coding = utf-8

__author__ = 'fly'

import logging
import asyncio
import aiomysql

# 将信息打印到控制台
def log(sql, args=()):
    logging.info('SQL: %s' % sql)
    # 打印info,warning,error,critical级别的日志

# create a link pool
async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool   # __pool私有全局属性
    __pool = await aiomysql.create_pool(
        host = kw.get('host', 'localhost'),
        port = kw.get('port', 3306),
        user = kw['user'],
        password = kw['password'],
        db = kw['db'],
        charset = kw.get('charset', 'utf-8'),
        autocommit = kw.get('autocommit', True),  # 默认自动提交事务
        maxsize = kw.get('maxsize', 10),
        minsize = kw.get('minsize', 1),
        loop = loop
    )
    '''
    create_pool(minsize, maxsize, loop=None,**kwargs) 协程，创建连接池，连接数据库。
    minsize,maxsize线程池大小,loop可选事件循环实例，若未循环，使用asyncio.get_event_loop()
    dict.get(key, default=None)返回指定键的值，如果值不在字典中，返回默认值。
    '''

# select in mysql
# sql查询语句字符串
# args 用来替换的参数
# size 返回查询结果的行数
async def select(sql, args, size=None):
    log(sql, args)   # 显示相应级别的信息
    global __pool
    with (await __pool) as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        # aiomysql.DictCursor返回字典类型的游标(cursor) 
        # conn.cursor() 获取指向连接的游标(cursor)
        # conn.cursor(aiomysql.DictCursor) 建立一个字典类型的游标
        await cur.execute(sql.replace('?', '%s'), args or ())
        # cur.execute(query, args=None)执行指定操作query
        # str.replace()
        if size:
            rs = await cur.fetchmany(size)
            # 一次性返回size条查询结果，结果是一个list,里面是tuple
        else:
            rs = await from cur.fetchall()
            # 返回所有查询结果
        await cur.close()
        # 关闭游标对象,不用手动关闭连接(conn)，因为是在with语句里面，会自动关闭
        # select不需要提交事务(commit)
        logging.info('rows returned: %s' % len(rs))
        # 打印信息，受影响的行数
        return rs

# insert, updata and delete in mysql
async def execute(sql, args, autocommit=True):
    log(sql)
    with (await __pool) as conn:
        if not autocommint:
            await conn.begin()
            # 开始数据库操作的协程 
        try:
            cur = await conn.cursor()
            # 获取指向连接的游标(cursor)
            await cur.execute(sql.replace('?', '%s'), args)
            # 
            affected = cur.rowcount
            await cur.close()
            # 关闭游标对象
            if not autocommit:
                await conn.commit()
                # 提交数据修改的协程
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
                # 回退到当前状态的协程
            raise
        return affected

def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)

class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)

class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        # 获取table名称
        tableName = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name, tableName))
        # 获取所有的Field和主键名
        mappings = dict()
        fields = []
        primaryKey = None
        for key, value in attrs.items():
            if isinstance(value, Field):
                logging.info(' found mapping: %s ==> %s' % (key, value))
                mappings[key] = value
                if value.primary_key:
                    # 找到主键
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for field: %s' % key)
                    primaryKey = key
                else:
                    fields.append(key)
        if not primaryKey:
            raise RuntimeError('primary key not found.')
        for key in mappings.keys():
            attrs.pop(key)
        escaped_fields = list(map(lambda f: '`%s`' % f, eields))
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey   # 主键属性名
        attrs['__fields__'] = fields          # 除主键外的属性名
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s ,`%s`) values (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, base, attrs)


class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        # getattr(object, name[, default]) # 用于返回object对象的name属性值。
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                # setattr(object, name, value) 用于设置object对象的name属性值为value，该数行必须存在
                setattr(self, key, value)
        return value
    
    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warn('failed to insert record: affecterd rows: %s' % rows)

    async def update(self):



    async def remove(self):


    async def findAll(self):


    async def findNumber():


if __name__ == "__main__":
    print("this is orm file")

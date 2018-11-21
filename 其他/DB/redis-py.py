from redis import StrictRedis, ConnectionPool

'''
每次都要。。
如下按顺序输入如下命令就可以连接成功.....
1. redis-cli.exe
2. shutdown
3. exit
4. redis-server.exe
'''

# 连接数据库
redis = StrictRedis(host='localhost', port=6379, db=0, password=None)

# 或
# pool = ConnectionPool(host='localhost', port=6379, db=0, password=None)
# redis = StrictRedis(connection_pool=pool)

# 或
# url = 'redis://localhost:6379/0'
# pool = ConnectionPool.from_url(url)
# redis = StrictRedis(connection_pool=pool)

print(redis)


# 设置一个键值对，然后获取它
redis.set('name', 'Bob')
print(redis.get('name'))

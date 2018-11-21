import pymongo
'''
需要每次搞这个。。。。
mongod.exe --dbpath c:\data\db
'''

# 建立DB链接
client = pymongo.MongoClient(host='localhost', port=27017)
# client = pymongo.MongoClient('mongodb://localhost:27017/')
print(client)

# 指定数据库"test"
db = client.test
# db = client['test']
print(db)

# 指定集合'students'（每个数据库里有许多集合collection，类似关系数据库中的表）
collection = db.students
# collection = db['students']
print(collection)


# 插入数据
student1 = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}
student2 = {
    'id': '20170202',
    'name': 'Mike',
    'age': 21,
    'gender': 'male'
}
student3 = {
    'id': '20170303',
    'name': 'july',
    'age': 19,
    'gender': 'female'
}
result = collection.insert_one(student1)
print(result)
results = collection.insert_many([student2, student3])
print(results)


# 单条查询
result = collection.find_one({'name': 'Mike'})
print(type(result))
print(result)

# 多条查询
results = collection.find({'age': 20})
print(results)
for _ in results:
    print(_)

# 条件查询
results = collection.find({'age': {'$lte': 20}})
print(results)
print(results.count())
for _ in results:
    print(_)

# 查询数据条数
count = collection.find().count()
print(count)

# 排序
results = collection.find().sort('name', pymongo.ASCENDING)
print([_['name'] for _ in results])

# 偏移，忽略前几个数据
results = collection.find().sort('name', pymongo.ASCENDING).skip(2)
print([_['name'] for _ in results])

# 也可以指定获取数据的个数
results = collection.find().sort('name', pymongo.ASCENDING).limit(2)
print([_['name'] for _ in results])

# 当数据量非常庞大时，不要使用大的偏移量，因为可能导致内存溢出。可以使用ObjectId来查询，但这需要记住id。。。
from bson.objectid import ObjectId
results = collection.find({'_id': {'$lte': ObjectId('5b9cc414f6003e2444ede5dc')}})
print(([_ for _ in results]))

# 更新
condition = {'name': 'july'}
student = collection.find_one(condition)
student['age'] = 18
result = collection.update_one(condition, {'$set': student})
print(result)
print(result.matched_count, result.modified_count)

# 删除
result = collection.delete_one({'name': 'july'})
print(result)
print(result.deleted_count)
result = collection.delete_many({'age': {'$gt': 19}})
print(result.deleted_count)

# 清空
result = collection.remove()
print(result)



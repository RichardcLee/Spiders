import pymysql


db = pymysql.connect(host='localhost', user='root', password='819555147', port=3306, db='test')
cursor = db.cursor()

cursor.execute('Select version()')
data = cursor.fetchone()
print('version:', data)

cursor.execute('create table if not exists students(id varchar(20) not null, age int not null, primary key(id))')

id = '100001'
age = 22
sql = 'insert into students values(%s, %s)'
try:
    cursor.execute(sql % (id, age))
    db.commit()
except Exception as e:
    print(e)
    db.rollback()

db.close()

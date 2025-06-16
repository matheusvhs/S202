import redis

r = redis.Redis(host='localhost', port=6379, db=0)

r.hset('user-session:123', mapping={
    'name': 'John',
    "surname": 'Smith',
    "company": 'Redis',
    "age": 29
})
# True

r.hgetall('user-session:123')
# {'surname': 'Smith', 'name': 'John', 'company': 'Redis', 'age': '29'}

r.hget('user-session:123', 'name')

selectAll = r.hgetall('user-session:123')
for key, value in selectAll.items():
    print(f"{key.decode('utf-8')}: {value.decode('utf-8')}")


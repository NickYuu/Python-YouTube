from common.database import Database

Database.initialize()
Database.insert('users', {"account": "nickyu", "pwd": "123456", "name":"Nick"})
user = Database.find_one('users', {"account": "nickyu"})
print(user)

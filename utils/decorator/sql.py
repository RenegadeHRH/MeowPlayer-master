# author: HRH

# date: 2022/3/7

# PyCharm
import pymysql
import json
import sys
with open(sys.path[1]+'/config/database.json','r') as f:
    f=json.load(f)
    host=f['host']
    username=f['username']
    password = f['password']
    database=f['database']
def conn():
    return pymysql.connect(host=host,
                         user=username,
                         password=password,
                         database=database)
def connectAndDisconnect(func):
    def wrapper(*args):
        db=pymysql.connect(host=host,
                         user=username,
                         password=password,
                         database=database)
        res=func(db,*args)
        db.close()

        return res

    return wrapper
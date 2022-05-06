# author: HRH

# date: 2022/4/30

# PyCharm
import sqlite3


class config:
    def __init__(self):
        self.path = r'F:\桌面\毕设\MusicRecommend\db.sqlite3'


SQLconfig = config()


def connectSQLite():
    return sqlite3.connect(SQLconfig.path)
def disconnectSQLite(sqldb):
    return sqldb.close()
def connAndDisConn(func):
    def wrapper(*args):

        db = connectSQLite()
        res = func(db, *args)

        db.close()
        return res
    return wrapper
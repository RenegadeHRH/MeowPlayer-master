# author: HRH

# date: 2022/3/7

# PyCharm
import utils.sql.getSQLdata as sql
import pymysql


def buildDatabase():
    loginInfo = sql.sqlData()
    db = pymysql.connect(
        host=loginInfo.host,
        user=loginInfo.userName,
        password=loginInfo.password
    )
    cursor = db.cursor()
    try:
        cursor.execute('use ' + loginInfo.database)
    except pymysql.err.OperationalError:
        cursor.execute('create schema ' + loginInfo.database)


if __name__ == '__main__':
    buildDatabase()

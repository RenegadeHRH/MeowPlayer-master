# author: HRH

# date: 2022/3/7

# PyCharm
import json
import sys

import pymysql
import utils.sql.getSQLdata as sql
SQLDATA=sql.sqlData()
db=pymysql.connect(host=SQLDATA.host,
                         user=SQLDATA.userName,
                         password=SQLDATA.password)
print(db)
db.close()
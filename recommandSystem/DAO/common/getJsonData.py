# author: HRH

# date: 2022/4/20

# PyCharm
import utils.sql.getSQLdata as database
from DBUtils.PooledDB import PooledDB
db=database.sqlData()
pool = PooledDB(pymysql, host=MYSQL_DB_HOST, user=MYSQL_DB_USER, passwd=MYSQL_DB_PWD, db='adinsights_v3', port=3306,
                charset="utf8", cursorclass=pymysql.cursors.SSCursor)


# author: HRH

# date: 2022/4/30

# PyCharm
from updateSQLite3.utils.Connection import connAndDisConn


@connAndDisConn
def search(db, table, field, val):
    sql = 'select * from {} whrere {} = "{}"'.format(table, field, val)
    cur = db.cursor()
    res = cur.execute(sql)
    db.commit()
    return res


def excutor(db, sql):
    cursor = db.cursor()
    res = cursor.execute(sql)
    db.commit()
    return res


def update(cur, table, id, field, val):
    if type(field) == list:
        sql = "UPDATE {} SET ".format(table)
        count = 0
        for i in field:
            print(count)

            sql += i + " =" + val[count] + ","
            count += 1
        sql = sql[:-1]
        sql += ' Where id={}'.format(id)
    else:
        sql = 'UPDATE {} SET {} = {}  WHERE id={};'.format(table, field, val, id)
        print(sql)
    try:

        cur.execute(sql)
    except Exception as e:
        print(e)

    return


def insert(cur, table, val):
    sql = "INSERT INTO {}  VALUES (".format(table)
    for i in val:
        sql += str(i) + ','
    sql = sql[:-1]
    sql += ');'
    cur.execute(sql)

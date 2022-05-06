# author: HRH

# date: 2022/4/14

# PyCharm
import sys
from ctypes import WinError

from pymysql import IntegrityError

import utils.decorator.sql as sql


def _makeCursor(db):
    try:
        cursor = db.cursor()
    except WinError as e:
        print('数据库断开，重连中...')
        db = sql.conn()
        cursor = db.cursor()
        print('重连成功')
    return cursor


def _sqlExecutor(db, sql):
    cursor = _makeCursor(db)
    try:
        cursor.execute(sql)
        db.commit()
        return True
    except IntegrityError as e:
        print(sql + '\n执行失败 IntegrityError:')
        print(e)
        return False
    except Exception as e:
        print('Exception from func:' + sys._getframe().f_code.co_name + ' content: ' + str(e))
        db.rollback()
        return False


@sql.connectAndDisconnect
def insert(db, data: dict, table: str):
    """
    只能操作纯字符串的数据库，根据数据的长度动态存入数据库
    :param db:
    :param data: 一字典的形式传入数据
    :param table:
    :return:
    """
    sql = 'insert into ' + table + ' values ('
    for v in data.values():
        if type(v) is not str:
            v = str(v)

        v = v.replace("'", " ").replace(',', ' ').replace('(', ' ').replace(')', ' ').replace('\\', " ").replace(' ',
                                                                                                                 "")

        sql += ('"' + v + '",')
    sql = sql[0:len(sql) - 1] + ')'
    if _sqlExecutor(db, sql) == True:
        print("\033[0;32;40mID:{ID} 插入{table}成功\033[0m".format(ID=data['ID'],table=table))
        return True
    return False


@sql.connectAndDisconnect
def delete(db, data: dict, table: str):
    """

    :param db:
    :param data: 以字典的形式传入数据,必须带有id
    :param table: 要操作的表
    :return:
    """
    sql = 'delete from ' + table + ' where ID ="' + data['ID'] + '"'
    _sqlExecutor(db, sql)


@sql.connectAndDisconnect
def update(db, data: dict, table: str):
    """
    更新数据,存在则更新，不存在则插入
    :param db:
    :param data:
    :param table:
    :return:
    """
    sql = 'select * from ' + table + ' where ID="' + data['ID'] + '"'
    cursor = _makeCursor(db)
    if cursor.execute(sql) == 0:
        insert(data, table)
    else:
        res = cursor.fetchall()
        if res[0][-1] is None:
            delete(data, table)
            insert(data, table)


@sql.connectAndDisconnect
def replace(db, data: dict, table: str):
    """
    替换数据
    :param db:
    :param data:
    :param table:
    :return:
    """
    delete(data, table)
    insert(data, table)


@sql.connectAndDisconnect
def searchSingle(db, data: dict, table: str):
    """
    搜索单条数据
    :param db:
    :param data:
    :param table:
    :return:
    """
    sql = 'select * from ' + table + ' where ID="' + data['ID'] + '"'
    cursor = _makeCursor(db)
    try:
        cursor.execute(sql)
        res = cursor.fetchone()
        return res
    except Exception as e:
        print('执行失败:{}'.format(str(e)))
        return None

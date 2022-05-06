# author: HRH

# date: 2022/4/30

# PyCharm
from time import sleep

from  updateSQLite3.utils.SQLoperation import excutor
from  updateSQLite3.utils.Connection import connectSQLite

from updateSQLite3.utils.SQLoperation import update
from utils.music163.config import getMusic163
import opencc
M=getMusic163()
# t2s - 繁体转简体（Traditional Chinese to Simplified Chinese）
# s2t - 简体转繁体（Simplified Chinese to Traditional Chinese）
# mix2t - 混合转繁体（Mixed to Traditional Chinese）
# mix2s - 混合转简体（Mixed to Simplified Chinese）
def c2s(str):
    """
    繁体转换为简体
    :param str:
    :return:
    """
    cc=opencc.OpenCC('t2s')
    return cc.convert(str)
def s2c(str):
    """
    简体转换为繁体
    :param str:
    :return:
    """
    cc = opencc.OpenCC('s2r')
    return cc.convert(str)
def mix2t(str):
    """
    混合转繁体
    :param str:
    :return:
    """
    cc = opencc.OpenCC('mix2t')
    return cc.convert(str)
def mix2s(str):
    """
    混合转简体
    :param str:
    :return:
    """
    cc = opencc.OpenCC('mix2s')
    return cc.convert(str)
def search(M,record):
    res=M.search(record[1])
    try:
        for i in res['songs']:
            if i['ar'][0]['name'] in c2s(record[3]):
                print('找到')
                print(i)
                res=i
                return res
    except Exception:
        print('出错')
        print(res)

    return None
def updateMusicID(cur,record,newID):
    """
    record中歌曲名为[1]，歌手为[3]，ID为[0]
    :param record:
    :return:
    """

    update(cur,'music_music',record[0],'id',str(newID))

    print('更新成功')

def updateDislikes(cur,record,newMusicID):

    """
    record中歌曲名为[1]，歌手为[3]，ID为[0]
    :param record:
    :return:
    """
    update(cur,'music_userprofile_dislikes',record[0],'music_id',newMusicID)
def updateLikes(cur,record,newMusicID):
    update(cur,'music_userprofile_likes', record[0], 'music_id', newMusicID)
def updateOriData():
    db = connectSQLite()
    cursor=db.cursor()
    sql="select * from music_music"
    res=cursor.execute(sql)
    cur2=db.cursor()
    while True:
        record=res.fetchone()
        if record==None:break
        try:
            res1=search(M,record)
        except Exception:
            continue
        if res1==None:
            print('未找到:')
            print(record)
            continue

        try:
            updateMusicID(cur2,record,res1['id'])

            updateDislikes(cur2,record,res1['id'])
            updateLikes(cur2,record,res1['id'])
        except Exception:
            continue
    db.commit()
    db.close()
updateOriData()
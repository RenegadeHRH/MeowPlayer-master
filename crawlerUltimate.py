# author: HRH

# date: 2022/3/11

# PyCharm
import re
import sys
import time
from ctypes import WinError

import requests
from pymysql import IntegrityError

from utils.decorator.sql import conn
from utils.music163.config import getMusic163
from utils.tools.tools import muti_Threadify


def getRawData(page, para):
    url = 'https://music.163.com/discover/playlist/?order=hot&cat=' + para + '&limit=35&offset='
    headers = {
        "method": "GET",
        "authority": "music.163.com",
        "scheme": "https",
        "path": "/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=35",
        "sec-ch-ua": ''' Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"''',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "upgrade-insecure-requests": "1",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "sec-fetch-dest": "iframe",
        "referer": "https://music.163.com/",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookies":
            "'_ntes_nuid=135f2a035b68444b1d15490ae484ca86; NMTID=00OkOQm8C0Cwx7XRULikPoVSsmwswYAAAF3C8gShA; "
            "ntes_kaola_ad=1; _ntes_nnid=135f2a035b68444b1d15490ae484ca86,1644678854483; WEVNSM=1.0.0; "
            "WNMCID=pvtxdb.1645094428023.01.0; __snaker__id=8A1mteOzLzq5cdxi; _9755xjdesxxd_=32; "
            "timing_user_id=time_9Rp49IJMew; WM_NI=3RYwFYB%2F9OwXZzTyypClQLqSOqlg%2FPOUt7pbWkq3bGw1B7lXcKszq%2BWT"
            "%2BVcE7ylJhe30VfWuUwM8PFVCwnRAQ4OwribkPj6w9igN98FxTTNI0Hdxi20HvBORaaUTcvOTZzk%3D; "
            "WM_NIKE"
            "=9ca17ae2e6ffcda170e2e6eed1e97092aa84afbb4f8db08eb2c84e939a9aaaf17ef5ae9ebab2498db683d3f02af0fea7c3b92af18e9798c55382f1f7b0f6549aa69c9afc7c81b49fadf4598dafa488ae5c8d8bbcd8f36a95b5bfd4e14db5ef8ed8ef54a195bd9bf421958ce5b7e24ff5a7a4abeb6ff1f09a87d67f97a983d9d34e969db98fd14b93ec8198f163a2b5a08bb57dfbb7a9afbc3486a89cb5cd43f498ac99ec3af498baa3ce5aa3bf9bb5e27e8d8c969bea37e2a3; WM_TID=d5PvmvpcSIBAUBQQAAN7uvuAY2DLzM3n; JSESSIONID-WYYY=qxrr5wp2qAlDbV0XI%5CzFcgT%5CaZojUsyQNk4vzCsjkmW2ojf8zgtB%5Cv%2FyVy%5CoXXSqQTw%2BFzhhZcCna1A%2BA1sWPj%2BIyH%2BCQBy5wA57DP%2B56Y8%2FX571jD5vqGKRoqD%2FJehAW74xqqEIVZVDJ5ne1yIn1kN5DtS12EPt%2F24SkYq0C4T16D6%5C%3A1649140576895; _iuqxldmzr_=33; gdxidpyhxdE=%2FB1Swr%5C1Bbbvs%5Cz7UVdWfmGlmDXrqAyX%2BxuvW6C%2F7B5phZ5VU1hbOhI57Wr4VEUR%2FKUQPSJIw8%5CxK8ozSMnxyBs%2F1QnyBcssfU%2FN%2F5OM1yPinJoy5IHqumzzyHOygldKmh'"}
    res = requests.get(url + str(page), headers)

    return res.text


def fast_way(DUPLICATES):
    return list(set(DUPLICATES))


def parse(text):
    lists = re.findall('playlist\?id=[0-9]*" class="msk', text)
    res = []
    for i in lists:
        res += re.findall('[0-9]*', i)
        while '' in res:
            res.remove('')

    return fast_way(res)


def getPlayList(id):
    music163 = getMusic163()
    return music163.playlist(id)



def dumpList2DB(listID,*args):

    playList=getPlayList(listID)

    try:
        db = conn()
        cursor = db.cursor()
        if cursor.execute('select * from playlists where ID = "%s"' % (playList.id)) == 0:

            if playList.id == '0':
                return
            print("----------------------------------数据存入：", playList.id, playList.name)
            cursor.execute(
                'insert into playlists values ("%s","%s")' % (playList.id, playList.name.replace('"', ' ').replace('\\', " ")))
            db.commit()
            dumpMusic2DB(listID)
        else:
            print('歌单:'+str(playList.name)+",ID:%s 已经存在！"%playList.id)
    except Exception as e:
        print('Exception from func:'+sys._getframe().f_code.co_name+' content: ' + str(e))
        db.rollback()
    try:
        db.close()
    except Exception as e:
        print('关闭数据库时出错：' + str(e))
    return
def dumpMusic2DB(listID):

    @muti_Threadify
    def dumpFunc(musicList,listID):
        db=conn()
        try:

            cursor = db.cursor()

        except WinError as e:
            print('数据库断开，重连中')
            db = conn()
            cursor = db.cursor()

        sql = 'insert into musics values ("%s","%s","%s","%s")' % (
            musicList.id, str(musicList.name[0]).replace('"', " "), str(musicList.artist).replace('"', " "), re.findall('[0-9]+',str(listID))[0])
        try:
            cursor.execute(sql)
            db.commit()
            print('存入歌曲id:%s,曲名:%s,作者:%s,关联列表:%s'%(
            musicList.id, str(musicList.name[0]).replace('"', " "), str(musicList.artist).replace('"', " "), re.findall('[0-9]+',str(listID))[0]))
        except IntegrityError as e:
            print(e)
            print('歌曲:[' + str(musicList.name) + "]已存在")
            return
        except Exception as e:
            print('Exception from func:'+sys._getframe().f_code.co_name+' content: ' + str(e))
            db.rollback()

        db.close()
    music163=getMusic163()
    try :

        pl=music163.playlist(listID)
        musicList=[]

        for i in pl:
            musicList.append(i)
        dumpFunc(musicList,listID)



    except Exception as e:
        print('Exception from func:'+sys._getframe().f_code.co_name+' content: ' + str(e))



def run():
    all=['全部']
    languege=['欧美','韩语','日语','华语','粤语']
    style1=['流行','摇滚', '民谣' ,'电子', '舞曲' ]
    style2=['说唱', '轻音乐' ,'爵士', '乡村' ,'R%26B%2FSoul', '古典' ,'民族']
    style3=[ '英伦', '金属' ,'蓝调' ,'雷鬼' ,'世界音乐' ,'拉丁','New%20Age', '古风', 'Bossa%20Nova','后摇']
    scenes=['清晨','夜晚','学习' ,'工作', '午休', '下午茶', '地铁', '驾车', '运动', '旅行', '散步', '酒吧']
    emotions=['怀旧', '清新', '浪漫', '伤感', '治愈', '放松', '孤独', '感动', '兴奋', '快乐', '安静', '思念']
    subjects=['综艺', '影视原声', 'ACG', '儿童', '校园', '游戏', '70后', '80后', '90后', '网络歌曲', 'KTV', '经典', '翻唱', '吉他', '钢琴', '器乐', '榜单', '00后']
    catList=[all,languege,style1,style2,style3,scenes,emotions,subjects]


    for  object in catList:
        for ob1 in object:
            lists=[]
            for i in range(30):
                raw = getRawData(i, ob1)
                lists+=parse(raw)
            print(ob1+'--------------------------结束爬取-----------------------')
            print(lists)
            muti_Threadify(dumpList2DB)(fast_way(lists))
            time.sleep(10)
            print(ob1+'--------------------------结束存入-----------------------')


run()

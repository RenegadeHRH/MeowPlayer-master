# author: HRH

# date: 2022/3/7

# PyCharm
import time

import pycloudmusic163
import pymysql
import requests
import re
from multiprocessing import Process
from utils.decorator.sql import connectAndDisconnect
from music163.getMusicsFromList import dumpPlaylist
from utils.music163.config import getMusic163
def fast_way(DUPLICATES):
 return list(set(DUPLICATES))
@connectAndDisconnect
def getData(db,para):
    music163 = getMusic163()
    cursor = db.cursor()
    url = 'https://music.163.com/discover/playlist/?order=hot&cat='+para+'&limit=35&offset='
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
        "cookies": "_ntes_nuid=135f2a035b68444b1d15490ae484ca86; NMTID=00OkOQm8C0Cwx7XRULikPoVSsmwswYAAAF3C8gShA; "
                   "WM_TID=9%2B6zGWTLg0xFVRUQFAdufhCK4NFTnoqz; _iuqxldmzr_=32; ntes_kaola_ad=1; "
                   "_ntes_nnid=135f2a035b68444b1d15490ae484ca86,1644678854483; WNMCID=pvtxdb.1645094428023.01.0; "
                   "WEVNSM=1.0.0; __snaker__id=8A1mteOzLzq5cdxi; _9755xjdesxxd_=32; "
                   "gdxidpyhxdE=hxwMwiuX%2Fh0bpuUxEhbEh8ebMTTDNYOxS6XZOscj30fX8A9wMnKWO3mB85tN4pU7LTsyG2Uy5k%5C"
                   "%2BU54MkS6ptsLjwTlavBAr92c63bAL25b6eZ5fIJSxaqp%2BxOczREwqrppDhz9DRdlKLcnpW"
                   "%2BXuy6iXL2ChksbKBNJ3XL1GqIspaHrv%3A1646541820986; __csrf=9cbed56c774f4db0ebdd4aa15cb5ee32; "
                   "__remember_me=true; "
                   "MUSIC_U"
                   "=7288622e17b8e08ef46f00f539bf23a7b89c90964e105270260e5141598e5d65993166e004087dd3d78b6050a17a35e705925a4e6992f61dfe3f0151024f9e31; WM_NIKE=9ca17ae2e6ffcda170e2e6eeabfc68f890af82ef4596eb8ab3d84b928b8a84f57fab91e589d07da592bfa3fb2af0fea7c3b92af78dadbbc53c938ff8a9f28086bea298f0398bacf785e547b1afb783d4468c99a08bea80b5b700d8aa62aab9878bb33df794faafe53bbaa697b6e44fa2b5bed0ce5df2b1a09bb5699498c0a2b164f4ecbadad07e90a888b0c6489686bda4cb63bbea8bd1e56787eff8d4c73fbbb3a9bbbb398bf18aafce218b8b858bfc7df2a79bd1f637e2a3; WM_NI=5ScZF0QQ8HstFbnwm3It9dfMsqybQNHGPjktwi07%2BjjgIj075L6Nf1zzYUaEbkr%2FOW2oPz6cPHpA2h04v9MvLxHOGLVZsCHiy6E0fmE183D5ymgZ83I%2FFNO%2BIUKjyw2yU0w%3D; JSESSIONID-WYYY=HhAZs0nsrn3bl3m0bmK8qoezqohk9jaS21UDJ%5CJ5wUR9hGB7UazXEWMDxYktWDpVrN9VXgdk3bb7Qt%2Fvn9K2O7CPM3gFF2%2FlI8K40GsSmrvBvCun%2F%5C%5CZ79fs2wwAO5EQxcbbD2CUwTqfwaM31F%2Bs3Nq086x04dAvIbWoz812%5Cqlc5Gn9%3A1646585873635 "
    }
    lists = []
    for i in range(0, 20):
        res = requests.get(url + str(i * 35), headers)
        lists += re.findall('playlist\?id=[0-9]*" class="msk', res.text)
        print('检索词条：'+para+'，取得数据条目:'+str(len(lists)))

    for i in fast_way(lists):

        i = set(re.findall('[0-9]*',i))
        i.remove('')
        i=list(i)[0]
        while True:
            try:
                pl = music163.playlist(i)
                break
            except:
                continue

        try:
            if cursor.execute('select * from playlists where ID = "%s"' % (i)) == 0:
                if pl.id=='0':
                    continue
                print(para+"-数据存入：",pl.id, pl.name)
                cursor.execute('insert into playlists values ("%s","%s")' % (pl.id, pl.name.replace('"',' ')))
                db.commit()
                dumpPlaylist(db,music163,pl.id)

        except Exception as e:
            print('Exception from func:[getData] content: '+str(e))
            db.rollback()


if __name__ == '__main__':
    all=['全部']
    languege=['欧美','韩语','日语','华语','粤语']
    style1=['流行','摇滚','流行', '摇滚', '民谣' ,'电子', '舞曲' ]
    style2=['说唱', '轻音乐' ,'爵士', '乡村' ,'R%26B%2FSoul', '古典' ,'民族']
    style3=[ '英伦', '金属' ,'蓝调' ,'雷鬼' ,'世界音乐' ,'拉丁','New%20Age', '古风', 'Bossa%20Nova']
    scenes=['清晨','夜晚','学习' ,'工作', '午休', '下午茶', '地铁', '驾车', '运动', '旅行', '散步', '酒吧']
    emotions=['怀旧', '清新', '浪漫', '伤感', '治愈', '放松', '孤独', '感动', '兴奋', '快乐', '安静', '思念']
    subjects=['综艺', '影视原声', 'ACG', '儿童', '校园', '游戏', '70后', '80后', '90后', '网络歌曲', 'KTV', '经典', '翻唱', '吉他', '钢琴', '器乐', '榜单', '00后']
    catList=[all,languege,style1,style2,style3,scenes,emotions,subjects]
    for i in catList:
        for j in i:
            getData(j)



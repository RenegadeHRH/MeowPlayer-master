# author: HRH

# date: 2022/4/14

# PyCharm
import re
import time

import requests

from crawlers.cloudMusic.utils.database import insert, searchSingle, update, replace
from utils.music163.config import getMusic163
from utils.tools.tools import muti_Threadify

tableName = 'playlistswithcategory'
"""
entity:playlists
paramOrder:ID,name,category
"""
all = ['全部']
languege = ['欧美', '韩语', '日语', '华语', '粤语']
style1 = ['流行', '摇滚', '民谣', '电子', '舞曲']
style2 = ['说唱', '轻音乐', '爵士', '乡村', 'R%26B%2FSoul', '古典', '民族']
style3 = ['英伦', '金属', '蓝调', '雷鬼', '世界音乐', '拉丁', 'New%20Age', '古风', 'Bossa%20Nova', '后摇']
scenes = ['清晨', '夜晚', '学习', '工作', '午休', '下午茶', '地铁', '驾车', '运动', '旅行', '散步', '酒吧']
emotions = ['怀旧', '清新', '浪漫', '伤感', '治愈', '放松', '孤独', '感动', '兴奋', '快乐', '安静', '思念']
subjects = ['综艺', '影视原声', 'ACG', '儿童', '校园', '游戏', '70后', '80后', '90后', '网络歌曲', 'KTV', '经典', '翻唱', '吉他', '钢琴', '器乐',
                '榜单', '00后']
categories = [all, languege, style1, style2, style3, scenes, emotions, subjects]

def getRawData(page, para):
    url = 'https://music.163.com/discover/playlist/?order=hot&cat=' + para + '&limit=35&offset='
    headers = {
        "method": "GET",
        "authority": "music.163.com",
        "scheme": "https",
        "path": "/discover/playlist/",
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
        "cookies":"_ntes_nuid=135f2a035b68444b1d15490ae484ca86; NMTID=00OkOQm8C0Cwx7XRULikPoVSsmwswYAAAF3C8gShA; ntes_kaola_ad=1; _ntes_nnid=135f2a035b68444b1d15490ae484ca86,1644678854483; WEVNSM=1.0.0; WNMCID=pvtxdb.1645094428023.01.0; __snaker__id=8A1mteOzLzq5cdxi; _9755xjdesxxd_=32; timing_user_id=time_9Rp49IJMew; _ns=NS1.2.325810498.1649785094; __csrf=d89ce9fb6f6289ae317ec5e2dd5714c9; MUSIC_U=7288622e17b8e08ef46f00f539bf23a7d82de61c0d761e8589f814ab7007836e993166e004087dd31115d7846a92ffee53856f0613fc69ae46b14e3f0c3f8af929f5e126cc9926cbc3061cd18d77b7a0; __remember_me=true; gdxidpyhxdE=mbwbHSfiwXS1eUzb50LY65bJlAmoLYUGbux9g54p49vfe8z6NBy6js1N%5C7TE5CGCC28fHJg%2F13wW687zJ3NLE0i1t%2BSm5tHm%2FKppCzAIs0BzQGKKvruLO3lGE%2FX%2F0jnnch5U4VcVe6UxGV1yJRNcr1%2F4NrL1DjdSqTl%2FEz2lKOUKOEL5%3A1649876557191; _iuqxldmzr_=32; WM_TID=e2NGbQm7TSZAAEVAFQfVAU1%2B1zr%2Bbtlv; WM_NI=hS9SRfYoLvmfHHmxYdzrpu%2BwjIBw%2B3WX0l5qjxeLOaJJINImHn3IqJyDSLGfJpd%2F2yJNj8ECvkCohIBeQKFQszjIDOZYVW4da8BArsGCGHbCWX8n6MMZMrxi8t5LyqUQSFM%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea9bb64b4ea97d8e567f5b08fb3c15f939e9eacc44b818a879bb66ea2e9a291aa2af0fea7c3b92aac8df7b4d16e9bb18497f06e8c98a399dc70baaec096aa7daa978e98aa399588008db87baaa8abadce6b8a9687afcc678cb2fdaaf442bb9c9dadc66e8ab0acd0b1738a92a6d9c849b6b58d90eb4382bb9facc55bb1a6a6aac7459a879ab8b770a3e88ea2f179859d89a9e1499588f88fb5478f868393fb63fcacfbadfc7b978f9da7d037e2a3; JSESSIONID-WYYY=ooNSeTEt982igBzlfcJc7sl%2BIXdrj8IHoPfSd3bFzsCFXohyIkco%2ByJvKEAlKtIDVKiDMkfeAvqKXvzUKQs3Z2MWKJgTtcU4Ar20%2BCofiDAohMy2EYZk1VPh19ql3UEEOVoDeD8G6d4uDupX9z7QzJECgI8M7KuUY%2F50iW2e9%5CQINpVz%3A1650419861594"
    }
    res = requests.get(url + str(page), headers)
    while res.history:
        print('等待1min')
        time.sleep(60)
        print(res.history)
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


def insertData(pl, category):

    insert(pl, tableName)
@muti_Threadify
def dumpData(musicListID,category):
    """
    当多线程执行的时候，传入的是一个list，这个list保存多个id
    :param musicList:
    :param catagory:
    :return:
    """
    playlist = getPlayList(musicListID)
    pl = {'ID': musicListID, 'name': playlist.name.replace('"', ' ').replace('\\', " "), 'category': str(category).replace("'"," ").replace(',',' ').replace('(',' ').replace(')',' ').replace('\\', " ").replace(' ',"")}
    if insertData(pl,category)==True:
        return True
    else:
        cates=searchSingle(pl,tableName)[-1]

        if str(category).replace("'"," ").replace(',',' ').replace('(',' ').replace(')',' ').replace('\\', " ").replace(' ',"") in cates:
            return True
        pl['category'] = cates + '、' + pl['category']

        replace(pl,tableName)
        return True

def run():

    # for l in categories:
    #     for i in l:
    #         musicList = parse(getRawData(1, i))
    for object in categories:
        for ob1 in object:
            lists = []
            print('----------------------分类:{}----------------------------'.format(ob1))
            for i in range(14):
                print('-----------------------page {} ------------------------'.format(i))
                raw = getRawData(i, ob1)
                lists += parse(raw)
            print('筛滤前{}'.format(lists))
            lists=fast_way(lists)
            print('取得热门歌曲列表:{}'.format(lists))

            dumpData(lists, ob1)
    # for i in categories:
    #     for j in i:
    #         for k in range(35):
    #             print('-----------------------page {} ------------------------'.format(k))
    #             musicList = parse(getRawData(k, j))
    #             print('----------------------分类:{}----------------------------'.format(j))
    #             print('取得热门歌曲列表:{}'.format(musicList))
    #             dumpData(musicList,j)
    #             print('----------------------dump结束---------------------------')
while True:
    run()
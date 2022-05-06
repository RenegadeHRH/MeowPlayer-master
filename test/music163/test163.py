# author: HRH

# date: 2022/3/6

# PyCharm
import random
import time
import pymysql

db = pymysql.connect(host='localhost',
                     user='root',
                     password='root',
                     database='163crawler')
cursor=db.cursor()
import pycloudmusic163
headers = pycloudmusic163.Music163.music163_headers
headers["cookie"] += "135f2a035b68444b1d15490ae484ca86"
music163 = pycloudmusic163.Music163(headers=headers)
# playlist = music163.playlist("6843808070") # 歌单id
# # 打印歌单标题 歌单作者 歌单简介
# print(playlist.name, playlist.user_str, playlist.description)
# for music in playlist:
#     # 打印歌单每一首歌的标题 歌手
#     print(music.name_str, music.artist_str)
with open('list5.txt','r',encoding='utf16') as f:

    data=f.readlines()
count=0
data=list(set(data))
print(data)
for i in data:
    i=i[12:22]
    data[count]=i
    count=count+1
for i in data:
    #
    # pl = music163.playlist(i)
    # cursor.execute("insert into playlists values %s,%s" % (pl.id, pl.name))
    # print(pl.name, pl.id)
    try:
        pl=music163.playlist(i)

        cursor.execute('insert into playlists values ("%s","%s")'%(pl.id,pl.name.replace('"',' ')))
        print(pl.name,pl.id)
        db.commit()
    except:
        db.rollback()
db.close()
    # time.sleep(random.randint(40,70))

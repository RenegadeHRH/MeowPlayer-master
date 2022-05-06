# author: HRH

# date: 2022/3/7

# PyCharm
from utils.decorator.sql import connectAndDisconnect
from utils.music163.config import getMusic163
from  pymysql.connections import Connection
import pycloudmusic163
def dumpPlaylist(db:Connection,music163,id):
    playlist=music163.playlist(id)
    for music in playlist:
        cursor=db.cursor()
        sql='insert into musics values ("%s","%s","%s","%s")'%(music.id,str(music.name[0]).replace('"'," "),str(music.artist).replace('"'," "),id)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()
            continue
        print(music.name[0],music.id,music.artist,id)
@connectAndDisconnect
def getMusicsFromList(db:Connection):
    cursor=db.cursor()
    total=cursor.execute('select * from playlists')
    music163=getMusic163()
    try:
        for count in range(14390,total-10,10):
            cursor.execute('select id from playlists limit %s,10' % str(count))
            res=cursor.fetchall()
            for i in res:
                dumpPlaylist(db,music163,i[0])
    except Exception as e:

        print(e)

getMusicsFromList()

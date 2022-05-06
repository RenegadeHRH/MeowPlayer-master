# author: HRH

# date: 2022/3/6

# PyCharm
import cloudmusic
import time
import random
if __name__ == '__main__':
    with open('list.txt','r',encoding='utf16') as f:

        data=f.readlines()
    count=0

    for i in data:
        i=i[12:22]
        data[count]=i
        count=count+1

    for i in data:

        pl=[]
        try:
            pl=cloudmusic.getPlaylist(i)

        except:
            print('erro in playlist:'+str(i))
            with open('leak.txt','a') as f:
                f.write(str(i)+'\n')
        time.sleep(random.randint(40,70))
        print(i)
        print(pl)

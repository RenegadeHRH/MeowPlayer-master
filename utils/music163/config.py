# author: HRH

# date: 2022/3/7

# PyCharm
import json

import pycloudmusic163
import sys
def getMusic163():
    headers=pycloudmusic163.Music163.music163_headers
    with open(sys.path[1]+'\\config\\music163.json','r') as f:
        headers['cookoe']=json.load(f)["cookie"]
    return pycloudmusic163.Music163(headers=headers)
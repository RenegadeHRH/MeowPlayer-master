# author: HRH

# date: 2022/3/11

# PyCharm
import re

import requests

from utils.decorator.sql import connectAndDisconnect
from utils.music163.config import getMusic163
import crawlers.cloudMusic.utils.database as db1
dic={'ID':'935437006','name':'龙俊亨◆诗人般的音乐者/创作合集/持更♪','catagory':''}
# dic2={'ID':'100007097'}
# dic3={'ID':'511211212'}
# # db1.insert(dic,'playlists')
# # db1.delete(dic,'playlists')
# db1.update(dic,'playlists')
# print(db1.searchSingle(dic,'playlistswithcategory'))
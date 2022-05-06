# author: HRH

# date: 2022/3/7

# PyCharm
import json
import sys
with open(sys.path[1]+'/config/database.json','r') as f:
    print(json.load(f)['host'])
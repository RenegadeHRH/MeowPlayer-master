# author: HRH

# date: 2022/3/7

# PyCharm
import json
import sys

class sqlData:
    def __init__(self):
        with open(sys.path[1] + '/config/database.json', 'r') as f:
            f = json.load(f)
        self.host=f['host']
        self.userName=f['username']
        self.password=f['password']
        self.database=f['database']


# author: HRH

# date: 2022/3/8

# PyCharm
from utils.decorator.funcAnalyze import culTime
@culTime
def test():
    for i in range(100):
        print(i)
test()
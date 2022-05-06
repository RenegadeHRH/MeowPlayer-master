# author: HRH

# date: 2022/3/8

# PyCharm
import time
def culTime(func):
    def wrapper(*args):
        t1=time.time_ns()
        res=func(*args)
        t2=time.time_ns()
        print('Func:'+func.__name__+',   cumsum time:'+str(t2-t1)+'ns')
        return res
    return wrapper
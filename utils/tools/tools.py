# author: HRH

# date: 2022/3/11

# PyCharm
import threading

threadCount=10
def listSlicer(list:list,sliceCount):
    #列表分割，供多线程多进程使用
    total = len(list)
    sliceLen = int(total / sliceCount)
    j = 0

    for i in range(0, total, sliceLen):

        if sliceLen*sliceCount<total and j== sliceCount-1:
            yield list[i:total]
        yield list[j*sliceLen:i+sliceLen]
        j += 1
class muti_Thread(threading.Thread):
    def __init__(self,threadID,target=None,*args):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.func=target
        self.args=args
    def run(self):
        print('线程：编号-'+str(self.threadID)+'，开始,数据处理量:%d'%len(self.args[0]))

        if type(self.args[0]) == list:
            for i in self.args[0]:

                self.func(i,self.args[1:])
        else:
            self.func(self.args)
        print('线程:编号-%d，结束'%self.threadID)

def muti_Threadify(func):

    def wrapper(list, *args):
        ls=listSlicer(list,threadCount)
        threads =[]
        if len(list)<threadCount:
            # 小于线程数的数据直接一次性处理
            j=0
            for i in list:
                thread=muti_Thread(j,func,i,args)
                thread.start()
                threads.append(thread)
                j+=1
            for t in threads:
                t.join()
        else:
            # 大于线程数的数据分片处理
            for i in range(threadCount):
                listSlice=next(ls)
                # print(listSlice)
                thread=muti_Thread(i,func,listSlice,args)
                thread.start()
                threads.append(thread)
            for t in threads:
                t.join()
        return
    return wrapper
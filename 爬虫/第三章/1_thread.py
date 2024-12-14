from threading import Thread


#创建线程
#Thread(target,args)：target线程执行的任务，args执行任务需要的参数，必须为元组类型的否则异常

def func(name):
    for i in range(10):
        print(name + " " + str(i))



class MyThread(Thread):
    def run(self):
        func('thread-2')


#，代表此为元组类型，否则因为元素只有一个，解释器会认为其是字符串
t = Thread(target=func, args=("thread-1",))
t.start()

mythread = MyThread()
mythread.start()
for i in range(10):
    print(str(i))



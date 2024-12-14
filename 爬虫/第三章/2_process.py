from multiprocessing import Process


def func(name):
    for i in range(1000):
        print(name + " " + str(i))

#，代表此为元组类型，否则因为元素只有一个，解释器会认为其是字符串
if __name__ == '__main__':
    p = Process(target=func,args=("process-1",))
    p.start()
    for i in range(1000):
        print(str(i))
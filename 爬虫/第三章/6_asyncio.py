import time
import asyncio

#async 标记这是协程函数

async def fun1():
    print('fun1 start')
    # time.sleep(2)   #直接执行三个 需要9s多
    await asyncio.sleep(2)  #await 关键字，挂起去执行其他协程 需要4s多 (只能放在协程函数里面)
    print('fun1 end')

async def fun2():
    print('fun2 start')
    # time.sleep(4)
    await asyncio.sleep(4)  #await 关键字，挂起去执行其他协程
    print('fun2 end')

async def fun3():
    print('fun3 start')
    # time.sleep(3)
    await asyncio.sleep(3)
    print('fun3 end')

async def main():
    pass

if __name__ == '__main__':
    task1 = fun1()  #并不会直接执行函数体内容，而是生成一个协程对象（类似于地址）
    task2 = fun2()
    task3 = fun3()

    task4 = main()
    # asyncio.run(task4)

    #执行单个task
    # asyncio.run(task1)  #执行协程对象对应的地址片段代码

    tasks = [task1, task2, task3]

    #执行多个task
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    start = time.time()
    loop.run_until_complete(asyncio.gather(*tasks))
    end = time.time()
    print(end - start)
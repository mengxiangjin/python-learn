from concurrent.futures import ThreadPoolExecutor,as_completed
import time
def func(name):
    for i in range(100):
        print(name + " " + str(i))

if __name__ == '__main__':
    task_list = []
    pools = ThreadPoolExecutor(5)
    for i in range(5):
        task_list.append(pools.submit(func, name=f'线程{i}'))

    # 阻塞主进程
    for result in as_completed(task_list):
        data = result.result()
    print("end")


    #会阻塞主线程，最后打印end
    # with ThreadPoolExecutor(max_workers=50) as executor:
    #     for i in range(100):
    #         executor.submit(func, name=f'线程{i}')
    # print('end')


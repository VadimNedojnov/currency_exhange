from time import sleep, time
import threading as tr
import requests
import os
from multiprocessing.pool import ThreadPool
import multiprocessing

processes_count = multiprocessing.cpu_count() * 2
print(processes_count)

#
#
# def foo(num):
#     print(tr.current_thread())
#     sleep(2)
#     print(num)
#
#
# start = time()
# thr1 = tr.Thread(target=foo, args=(1, ))
# thr2 = tr.Thread(target=foo, args=(2, ))
#
# thr1.start()
# thr2.start()
#
# thr1.join()
# thr2.join()
#
# print(f'Done in: {time() - start}')


# def foo(num):
#     # print(tr.current_thread())
#     sleep(num)
#
#
# # start = time()
# threads = []
# for i in range(10):
#     thr1 = tr.Thread(target=foo, args=(i, ))
#     thr1.start()
#     threads.append(thr1)
#
#
# while threads:
#     print(len(threads), threads)
#     sleep(0.5)
#     for index, th in enumerate(threads):
#         if not th.is_alive():
#             threads.pop(index)
#
# print('Done')

# def save_image():
#     url = 'https://loremflickr.com/320/240/dog'
#     response = requests.get(url)
#     name = response.url.split('/')[-1]
#     path = os.path.join(os.getcwd(), 'images', name)
#
#     with open(path, 'wb') as file:
#         file.write(response.content)
#
#
# start = time()
# threads = []
# for _ in range(100):
#     t = tr.Thread(target=save_image)
#     t.start()
#     threads.append(t)
#
# for th in threads:
#     th.join()
# print(time() - start)

# def save_image(*args):
#     url = 'https://loremflickr.com/320/240/dog'
#     response = requests.get(url)
#     name = response.url.split('/')[-1]
#     path = os.path.join(os.getcwd(), 'images', name)
#
#     with open(path, 'wb') as file:
#         file.write(response.content)
#
#
# start = time()
# with ThreadPool(25) as pool:
#     pool.map(save_image, range(100))
# print(time() - start)


# COUNT = 500_000_000
#
#
# def countdown(n):
#     while n > 0:
#         n -= 1
#
#
# start = time()
# # countdown(COUNT)
# processes = []
#
# for i in range(processes_count):
#     p1 = multiprocessing.Process(target=countdown, args=(COUNT // processes_count, ))
#     p1.start()
#     processes.append(p1)
#
# for p in processes:
#     p.join()
#
#
# print(time() - start)



import socket
from threading import Thread
import psutil
from time import sleep
from datetime import datetime


sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock1.connect(('localhost', 9999))
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2.connect(('localhost', 9999))


class Memory:
    def __init__(self):
        self.memory = 0

    def collect_values(self):
        self.memory = psutil.virtual_memory().available / 1_048_576
        self.draw_results()

    def draw_results(self):
        temp = "Available memory: " + str(self.memory)
        sock2.send(temp.encode('utf-8'))
        sleep(60)
        self.collect_values()


class Cpu_info:
    def __init__(self):
        self.count_process = 0
        self.cpu_percent = 0

    def collect_values(self):
        self.count_process = len(list((psutil.process_iter())))  # количество запущенный процессов
        self.cpu_percent = psutil.cpu_percent(interval=None, percpu=False)  # нагрузка цп в процентах
        self.draw_results()

    def draw_results(self):
        temp = "Count process: " + str(self.count_process)
        sock1.send(temp.encode('utf-8'))
        sleep(60)
        self.collect_values()


Thread_CPU = Cpu_info()
Thread_Memory = Memory()
thread1 = Thread(target=Thread_CPU.collect_values, daemon=True)
thread2 = Thread(target=Thread_Memory.collect_values, daemon=True)
thread1.start()
thread2.start()
thread1.join()
thread2.join()

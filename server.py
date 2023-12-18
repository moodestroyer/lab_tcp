import csv
import socket
from datetime import datetime
from multiprocessing.pool import ThreadPool


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('localhost', 9999))
sock.listen(10)  # длина очереди


def handler(client):
    while True:
        data = client.recv(1024)
        now = datetime.now()
        with open("output.csv", 'a') as file:
            csv.writer(file, lineterminator="\r").writerow([now.strftime("%H:%M:%S"), data.decode('utf-8')])


pool = ThreadPool(4)
while True:
    client1, addr = sock.accept()
    print('Connected:', addr)
    pool.apply_async(handler, (client1,))

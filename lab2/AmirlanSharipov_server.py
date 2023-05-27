import os
import socket
import time
import random
import threading
import io

from PIL import Image

SERVER_URL = '0.0.0.0:1234'
FRAME_COUNT = 5000
BACKLOG = 100


def routine_send_img(connection):
    img = Image.new(mode="RGBA", size=(10, 10))
    pix = img.load()
    for i in range(10):
        for j in range(10):
            r = random.randrange(0, 255)
            g = random.randrange(0, 255)
            b = random.randrange(0, 255)
            pix[i, j] = (r, g, b)

    output = io.BytesIO()
    img.save(output, format='PNG')
    connection.send(output.getvalue())
    connection.close()


def main():
    ip, port = SERVER_URL.split(':')
    port = int(port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))

    s.listen(BACKLOG)
    print(f'Listening on port {port}...')

    threads = list()
    while True:
        connection, addr = s.accept()
        #print(f'connected from {addr}...')

        t = threading.Thread(target=routine_send_img, args=(connection, ))
        threads.append(t)
        t.start()
        print(f'Sending an image to {addr}...')

    for t in threads:
        t.join()

    s.close()


if __name__ == '__main__':
    main()

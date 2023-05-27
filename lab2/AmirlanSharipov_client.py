# BEFORE CLIENT OPT:
# Frames download time: 4.928671836853027
# GIF creation time: 5.02190637588501
# AFTER CLIENT OPT:
# Frames download time: 3.885207176208496
# GIF creation time: 4.356576204299927

import os
import socket
import time
import threading
import multiprocessing

from PIL import Image

SERVER_URL = '127.0.0.1:1234'
FILE_NAME = 'AmirlanSharipov.gif'
CLIENT_BUFFER = 1024
FRAME_COUNT = 5000
MAXTHREADS = 8
MAXPROCESSES = 8

pool_sema = threading.BoundedSemaphore(value=MAXTHREADS)


def routine_save_image(i):
    with pool_sema:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            ip, port = SERVER_URL.split(':')
            s.connect((ip, int(port)))
            image = b''
            while True:
                packet = s.recv(CLIENT_BUFFER)
                if not packet:
                    break
                image += packet

            with open(f'frames/{i}.png', 'wb') as f:
                f.write(image)


def download_frames():
    t0 = time.time()
    if not os.path.exists('frames'):
        os.mkdir('frames')

    threads = list()
    for i in range(FRAME_COUNT):
        t = threading.Thread(target=routine_save_image, args=(i, ))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return time.time() - t0


def get_RGBA(fname):
    return Image.open(fname).convert('RGBA')


def create_gif():
    t0 = time.time()
    frame_list = list()
    for frame_id in range(FRAME_COUNT):
        frame_list.append(f'frames/{frame_id}.png')

    with multiprocessing.Pool(MAXPROCESSES) as p:
        frames = p.map(get_RGBA, frame_list)

    frames[0].save(FILE_NAME, format="GIF",
                   append_images=frames[1:], save_all=True, duration=500, loop=0)
    return time.time() - t0


if __name__ == '__main__':
    print(f"Frames download time: {download_frames()}")
    print(f"GIF creation time: {create_gif()}")

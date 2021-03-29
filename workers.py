from multiprocessing import Process
import time

WORKERS = {}
WORKER_ID = 0

def start_worker(id):
    while True:
        print('Worker: ', id)
        time.sleep(1)


def create_worker():
    global WORKERS
    global WORKER_ID

    proc = Process(target=start_worker, args=(WORKER_ID,))
    proc.start()
    WORKERS[WORKER_ID] = proc
    
    WORKER_ID += 1

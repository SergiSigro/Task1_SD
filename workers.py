from multiprocessing import Process
import time
import redis

WORKERS = {}
WORKER_ID = 0

def work_to_do(task, tareas):
    if not task:
        return
    else:
        #Analizar la tarea
        

def start_worker(id):
    keyCola="inst"
    print('Worker: ', id)
    tareas = redis.Redis(host='localhost', port=6379, db=0) #Creamos la conexión con la cola de tareas (servidor redis)
    while True:
        #Comprobar si tenemos tareas
        task=tareas.rpop(keyCola)
        work_to_do(task, tareas)
        time.sleep(2.5)


def create_worker():
    global WORKERS
    global WORKER_ID

    proc = Process(target=start_worker, args=(WORKER_ID,))
    proc.start()
    WORKERS[WORKER_ID] = proc
    
    WORKER_ID += 1

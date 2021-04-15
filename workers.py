from multiprocessing import Process
import time
import redis

WORKERS = {}
WORKER_ID = 0

#Separa los campos del string "dirty_task" y los mete en un diccionario que retorna
#Se asume que a estas alturas del programa los campos son todos correctos
def clean_task(dirty_task):
    fields = dirty_task.split(",")
    fields = { 'ID':fields[0], 'Operation':fields[1], 'File':fields[2], 'NumFiles':fields[3]}
    return fields

#Analiza la tarea
def work_to_do(task, tareas):
    if not task:
        return
    else:
        #Separamos los campos y los guardamos en un diccionario:
        polished_task = clean_task(task)
        
        
        

def start_worker(id):
    keyCola="inst"
    print('Worker: ', id)
    tareas = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True) #Creamos la conexión con la cola de tareas (servidor redis)
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

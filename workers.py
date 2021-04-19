from multiprocessing import Process
from flask import Flask
import time
import redis
import requests

WORKERS = {}
WORKER_ID = 0


def notify_redis(clean_task, results, result):
    if clean_task['NumFiles'] is '1':
        results.lpush(clean_task['ID'], result)
    if int(clean_task['NumFiles']) > 1:
        if results.llen(clean_task['ID']) < (int(clean_task['NumFiles']) - 1 ):
            results.lpush(clean_task['ID'], result)
        else:
            total=0
            for i in range(results.llen(clean_task['ID'])):
                total = total + int(results.rpop(clean_task['ID']))
            total = total + result
            results.lpush(clean_task['ID'], total)
            


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
        #fitxer = requests.get(polished_task['File'])
        #print('Llegint fitxer ubicat a '+polished_task['File']+' ----> ',fitxer.text)
        #EN fitxer.text HI HA EL TEXT DEL FITXER
        #ARA CALDRIA CRIDAR A LA FUNCIO CORRESPONENT
        if 'CountWords' in polished_task['Operation']:
            #CRIDAR A LA FUNCIO CountWords
            print('Hem toca CountWords---->',polished_task['Operation'])
        if 'WordCount' in polished_task['Operation']:
            #CRIDAR A LA FUNCIO wordCount
            print('Hem toca WordCount---->',polished_task['Operation'])
        #UNA VEZ OBTENGAMOS EL RESULTADO NOS TOCARA ACTUALIZAR REDIS
        result=5
        notify_redis(polished_task, tareas, result)

        
        
        

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

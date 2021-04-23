from multiprocessing import Process
from flask import Flask
import time
import redis
import requests
import instrucciones_SD

WORKERS = {}
WORKER_ID = 0


def is_error(n):
    try:
        if int(n) == -1:
            return True
        return False
    except ValueError:
        return False


def notify_redis(clean_task, results, result):
    correcto=True
    #print(clean_task)
    if clean_task['NumFiles'] is '1':
        results.lpush(clean_task['ID'], str(result))
        results.lpush(clean_task['ID'], clean_task['File'])
        results.lpush(clean_task['ID'], "done")
        
    if int(clean_task['NumFiles']) > 1:
        if results.llen(clean_task['ID']) < 2*(int(clean_task['NumFiles']) - 1 ):
            #print("Fichero no ultimo")
            results.rpush(clean_task['ID'], str(result))
            results.lpush(clean_task['ID'], clean_task['File'])
        else:
            total=0
            i=0
            fitx=""
            dic={}
            while i<int(clean_task['NumFiles'])-1:
                valor = results.rpop(clean_task['ID'])
                #print(valor)
                #print(is_error(valor))
                if is_error(valor):
                    correcto=False
                    fitx+=results.lpop(clean_task['ID'])+"\n"
                else:
                    if  'CountingWords' in clean_task['Operation']:
                        num=int(valor)
                        results.lpop(clean_task['ID'])
                        total = total + num
                    else:
                        subDic = eval(valor)
                        for subKey in subDic:
                            if subKey in dic:
                                dic[subKey] += subDic[subKey]
                            else:
                                dic[subKey] = subDic[subKey]
                        results.lpop(clean_task['ID'])
                i += 1
            if result == -1:
                correcto=False
            if correcto:
                if  'CountingWords' in clean_task['Operation']:
                    total = total +result
                    results.lpush(clean_task['ID'], total)
                else:
                    for subKey in result:
                        if subKey in dic:
                            dic[subKey] += result[subKey]
                        else:
                            dic[subKey] = result[subKey]
                    dic=sorted(dic.items())
                    results.lpush(clean_task['ID'], str(dic))
                results.lpush(clean_task['ID'], "done")
            else:
                if result == -1:
                    fitx+=clean_task['File']
                results.lpush(clean_task['ID'], -1)
                results.lpush(clean_task['ID'], fitx)
                results.lpush(clean_task['ID'], "done")


            #for i in range(results.llen(clean_task['ID'])):
            #    total = total + int(results.rpop(clean_task['ID']))
            #total = total + result
            #results.lpush(clean_task['ID'], total)
            #results.lpush(clean_task['ID'], "done")
            
            


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
        fitxer = requests.get(polished_task['File'])
        if fitxer.status_code != 404:
            #print('Llegint fitxer ubicat a '+polished_task['File']+' ----> ',fitxer.text)
            if 'CountingWords' in polished_task['Operation']:
                result = instrucciones_SD.countingWords(fitxer.text)
                #print('Hem toca CountWords---->',polished_task['Operation'])
            if 'WordCount' in polished_task['Operation']:
                #print('Hem toca WordCount---->',polished_task['Operation'])
                result = instrucciones_SD.wordCount(fitxer.text)
                #print(result)
            notify_redis(polished_task, tareas, result)
        else:
            
            result=-1
            notify_redis(polished_task, tareas, result)
        
        
        

def start_worker(id, tareas):
    keyCola="inst"
    print('Worker: ', id)
    # tareas = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True) #Creamos la conexión con la cola de tareas (servidor redis)
    while True:
        #Comprobar si tenemos tareas
        task=tareas.rpop(keyCola)
        
        work_to_do(task, tareas)
        time.sleep(2.5)


def createWorker(redis):
    global WORKERS
    global WORKER_ID

    proc = Process(target=start_worker, args=(WORKER_ID,redis))
    proc.start()
    WORKERS[WORKER_ID] = proc
    
    WORKER_ID += 1

def deleteWorker():
    global WORKERS
    global WORKER_ID

    WORKER_ID -= 1
    proc = WORKERS[WORKER_ID]
    proc.terminate()
    
    print("TERMINATED Worker: ", WORKER_ID)
    

def listWorkers():
    global WORKERS
    global WORKER_ID
    if WORKER_ID == 0:
        llistat = "No hi han workers."
    else:
        i=0
        llistat = "Workers:\n"
        while i < WORKER_ID:
            proc = WORKERS[i]
            llistat += "Worker "+str(i)+"\n"
            i += 1
    return llistat
        
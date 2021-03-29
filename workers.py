from multiprocessing import Process
import time

WORKERS = {}
WORKER_ID = 0

def start_worker(id,redis):
    while True:
        #pop de la cua del redis
        #Cosas que rebem:       Tasca, Fitxer, JOBID, num_fitxers
        #   Si 3 parametre no es fitxer fer suma (?) 
        #   Path 1: Ficar al redis resulat de la tasca amb la key de JOBID (?)
        #           
        # 
        #   Path 2: Veure quins workers tenen la mateixa JOBID (?)
        #           Comunicacio entre workers
        #           
        #   
        #   
        #   OBJECTIU SUMAR TOTS ELS RESULTATS!!!!
        # 
        pass   




def createWorker(redis):
    global WORKERS
    global WORKER_ID

    proc = Process(target=start_worker, args=(WORKER_ID,redis))
    proc.start()
    WORKERS[WORKER_ID] = proc
    
    WORKER_ID += 1

def deleteWorker():
    pass
def listWorkers():
    pass
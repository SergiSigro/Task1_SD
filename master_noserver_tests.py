import workers
import time
import redis

if __name__ == "__main__":
    
    #crear servidor redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushall()    #eliminamos todo lo que estuviese en el redis anteriormente

    keyCola = "inst"    #key de la cola de instrucciones
    JOB_ID=0    #numero del trabajo == key para obtener el resultado de la operacion

    workerManagement = ["createWorker", "deleteWorker", "listWorkers"]  #lista de comandos relacionados con la administracion de los workers
    programs = ["CountingWords", "WordCount"]   #lista de programas 
    while True:
        #recibir instrucciones del usuario
        print("Introduce un comando:")
        instruccion = input()
        instruccion = instruccion.split()
        
        
        #si instruccion esta relacionada con la administracion de los workers
        if instruccion[0] in workerManagement:
            if instruccion[0] == workerManagement[0]:
                workers.createWorker(r)
            elif instruccion[0] == workerManagement[1]:
                workers.deleteWorker()
            else:
                workers.listWorkers()
        

        #si instruccion es uno de los programas
        elif instruccion[0] in programs:
            JOB_ID += 1
            numFile=1
            while numFile < len(instruccion):
                tupla = (JOB_ID, instruccion[0], instruccion[numFile], len(instruccion)-1)
                r.lpush(keyCola, tupla)
                numFile += 1
            while r.lindex(JOB_ID, 0) != "done":
                pass
            print(r.lindex(JOB_ID, -1))
        
         
        #si instruccion no es valida
        else:
            print("Operacion incorrecta")
        
        
        
        
    pass


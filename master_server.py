from concurrent import futures

import time
<<<<<<< HEAD
import redis

if __name__ == "__main__":
    tareas = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    tareas.flushall()
    #Formato tareas:  (JOBID, CountWords/WordCount, http://localhost:8080/fitxer1.txt, numFiles)
    # Tareas cortas:
    tareas.lpush("inst", "1,CountWords,http://localhost:8000/fitxer1.txt,1")
    tareas.lpush("inst", "2,WordCount,http://localhost:8000/fitxer2.txt,1")
    #Jobs:
    tareas.lpush("inst", "3,WordCount,http://localhost:8000/fitxer2.txt,2")
    tareas.lpush("inst", "3,WordCount,http://localhost:8000/fitxer3.txt,2")
    tareas.lpush("inst", "4,CountWords,http://localhost:8000/fitxer3.txt,2")
    tareas.lpush("inst", "4,CountWords,http://localhost:8000/fitxer4.txt,2")
    #Jobs extensos:
    tareas.lpush("inst", "5,WordCount,http://localhost:8000/fitxer1.txt,4")
    tareas.lpush("inst", "5,WordCount,http://localhost:8000/fitxer2.txt,4")
    tareas.lpush("inst", "5,WordCount,http://localhost:8000/fitxer3.txt,4")
    tareas.lpush("inst", "5,WordCount,http://localhost:8000/fitxer2.txt,4")

    for i in range(5):
        workers.create_worker()
    pass

    time.sleep(10)
    print("Resultat tasca 1: ",tareas.lpop('1'))
    print("Resultat tasca 2: ",tareas.lpop('2'))
    print("Resultat tasca 3: ",tareas.lpop('3'))
    print("Resultat tasca 4: ",tareas.lpop('4'))
    print("Resultat tasca 5: ",tareas.lpop('5'))

=======
import math
import logging


import grpc

import MasterServer_pb2
import MasterServer_pb2_grpc

import redis
import workers


class MasterServerServicer(MasterServer_pb2_grpc.MasterServerServicer):
    #Functions
    def __init__(self):
        self.JOB_ID = 0 #numero del trabajo == key para obtener el resultado de la operacion
        self.NUM_WORKERS = 0 #numero de workers
        self.r = redis.Redis(host='localhost', port=6379, db=0)  #crear servidor redis
        self.r.flushall()    #eliminamos todo lo que estuviese en el redis anteriormente
        self.keyCola = "inst"    #key de la cola de instrucciones

    def GetResultatCW(self, request, context):
        files = request.fitxers.split()
        self.JOB_ID += 1
        numFiles = len(files)
        for i in files:
            tupla = (self.JOB_ID, "CountingWords", i, numFiles)
            self.r.lpush(self.keyCola, tupla)
        while self.r.lindex(self.JOB_ID, 0) != "done":
            pass
        resultat = self.r.lindex(self.JOB_ID, -1)
        self.r.delete(self.JOB_ID)
        return MasterServer_pb2.resultat(resultat="Total de paraules contades en els fitxers: " + str(files) + " = " + str(resultat))
    
    def GetResultatWC(self, request, context):

        files = request.fitxers.split()
        self.JOB_ID += 1
        numFiles = len(files)
        for i in files:
            tupla = (self.JOB_ID, "WordCount", i, numFiles)
            self.r.lpush(self.keyCola, tupla)
        while self.r.lindex(self.JOB_ID, 0) != "done":
            pass
        resultat = self.r.lindex(self.JOB_ID, -1)
        self.r.delete(self.JOB_ID)
        return MasterServer_pb2.resultat(resultat="Resultat de WordCount dels fitxers: " + str(files) + "\n" + resultat)

    def CreateWorker(self, request, context):
        i = 0
        while i < request.num:
            workers.createWorker(self.r)
            self.NUM_WORKERS += 1
            i += 1
        return MasterServer_pb2.resultat(resultat="Workers creats correctament.")

    def DeleteWorker(self, request, context):

        if request.num > self.NUM_WORKERS:
            return MasterServer_pb2.resultat(resultat="No es poden eliminar aquella cuantitat de workers.\nNumero de workers: "+str(self.NUM_WORKERS))
        i = 0
        while i < request.num:
            workers.deleteWorker()
            self.NUM_WORKERS -= 1
            i += 1
        return MasterServer_pb2.resultat(resultat="Workers eliminats correctament.")

    def ListWorkers(self, request, context):
        return MasterServer_pb2.resultat(resultat=workers.listWorkers())

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    MasterServer_pb2_grpc.add_MasterServerServicer_to_server(MasterServerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()    
>>>>>>> b7af416ffe15b629cf37e9dcf8d96cf101a8e0be

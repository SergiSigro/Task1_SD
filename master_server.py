from concurrent import futures

import time
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

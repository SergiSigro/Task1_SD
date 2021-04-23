from __future__ import print_function

import random
import logging
import sys

import grpc

import MasterServer_pb2_grpc
import MasterServer_pb2

def genNumero(numero):
    return MasterServer_pb2.numero(
        num=int(numero)
    )

def genInputFiles():
    files=sys.argv[3]
    if len(sys.argv) > 3:
        for i in sys.argv[4:]:
            files +=" "+i
    files = files.translate({ord(c): None for c in "[,]"})
    return MasterServer_pb2.input(fitxers=files)

def create_worker(stub, num):
    resultat = stub.CreateWorker(num)
    print(resultat.resultat)

def delete_worker(stub, num):
    resultat = stub.DeleteWorker(num)
    print(resultat.resultat)

def list_workers(stub):
    aux = MasterServer_pb2.empty()
    resultat = stub.ListWorkers(aux)
    print(resultat.resultat)

def word_count(stub, files):
    resultat = stub.GetResultatWC(files)
    print(resultat.resultat)

def count_words(stub, files):
    resultat = stub.GetResultatCW(files)
    print(resultat.resultat)

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = MasterServer_pb2_grpc.MasterServerStub(channel)
        if len(sys.argv) > 1:
            if sys.argv[1] == 'worker':
                if len(sys.argv) > 2:
                    if sys.argv[2] == 'create':
                        if len(sys.argv) != 4:
                            create_worker(stub, genNumero(1))
                        else:
                            create_worker(stub, genNumero(sys.argv[3]))
                    elif sys.argv[2] == 'delete':
                        if len(sys.argv) != 4:
                            delete_worker(stub, genNumero(1))
                        else:
                            delete_worker(stub, genNumero(sys.argv[3]))
                    elif sys.argv[2] == 'list':
                        list_workers(stub)
                else:
                    print("Pots crear un o més workers amb create.\nPots eliminar un o més workers amb delete.\nPots mostrar una llista dels workers amb list.")
            elif sys.argv[1] == 'job':
                if len(sys.argv) > 2:
                    if sys.argv[2] == 'run-wordcount':
                        if len(sys.argv) < 4:
                            print("Necesites introduir un fitxer de entrada.")
                        else:
                            word_count(stub, genInputFiles())
                    elif sys.argv[2] == 'run-countwords':
                        if len(sys.argv) < 4:
                            print("Necesites introduir un fitxer de entrada.")
                        else:
                            count_words(stub, genInputFiles())
                else:
                    print("Per comptar el nombre total de paraules en diferents fitxers utilitza run-countwords.\nPer comptar el nombre d'ocurrències de cada paraula utilitza run-wordcount.")
        else:
            print("Introduint worker com a primer paràmetre pots gestionar els workers.\nIntroduint job pots enviar una petició per a un treball.\nRecorda: per a enviar una petició de treball necessites tenir com a mínim un worker.")
if __name__ == '__main__':
    logging.basicConfig()
    run()

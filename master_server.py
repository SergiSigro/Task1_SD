import workers
import time
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


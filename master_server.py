import workers
import time
import redis

if __name__ == "__main__":
    tareas = redis.Redis(host='localhost', port=6379, db=0)
    tareas.flushall()
    tareas.lpush("inst", "Instruccion 1")
    tareas.lpush("inst", "Instruccion 2")

    for i in range(5):
        workers.create_worker()
    pass


import time

from celery import Celery

app = Celery('celery_task', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')


@app.task(name='celery_tasks.add')
def add(x, y):
    total = x + y
    print(f'{x} + {y} = {total}')
    time.sleep(10)
    return total

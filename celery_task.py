from celery import Celery

app = Celery('celery_task', backend=None, broker='redis://localhost:6379/0')


def add(x, y):
    print(f'{x} + {y} = {x + y}')

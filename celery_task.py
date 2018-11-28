import logging

import time

from celery import Celery

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)

app = Celery('celery_task', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')


@app.task(name='celery_tasks.add')
def add(x, y):
    total = x + y
    print(f'{x} + {y} = {total}')
    time.sleep(10)
    return total


def backoff(attempts):
    """
    1, 2, 4, 8, 16, 32, ...
    :param attempts:
    :return:
    """
    return 2 ** attempts

@app.task(bind=True, max_retries=20, soft_time_limit=1)
def data_extractor(self):
    log.info(f"Running {self.name}")
    try:
        for i in range(1, 11):
            print('Crawling HTML DOM!')
            if i == 5:
                raise ValueError('Crawling Index Error.')
    except Exception as exc:
        print('There was an error let try after 5 seconds.')
        log.exception(exc)
        raise self.retry(exc=exc, countdown=backoff(self.request.retries))


import logging

import time
from datetime import timedelta

from celery import Celery
from celery.task import periodic_task
from celery.schedules import crontab

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
    :param attempts: Current number of attempts
    :return: 2 ^ (n) where n is the number of attempts.
    """
    return 2 ** attempts


# @app.task(bind=True, max_retries=20, soft_time_limit=1)
# def data_extractor(self):
#     log.info(f"Running {self.name}")
#     try:
#         for i in range(1, 11):
#             print('Crawling HTML DOM!')
#             if i == 5:
#                 raise ValueError('Crawling Index Error.')
#     except Exception as exc:
#         print('There was an error let try after 5 seconds.')
#         log.exception(exc)
#         raise self.retry(exc=exc, countdown=backoff(self.request.retries))


@periodic_task(run_every=timedelta(seconds=5), name='celery_task.send_mail_from_queue')
def send_mail_from_queue():
    try:
        message = 'example.email'
        print(f'Email Sent successfully, [{message}]')
    finally:
        print('release resources')

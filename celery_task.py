import logging

import time
from datetime import timedelta
import redis

from billiard.exceptions import SoftTimeLimitExceeded
from celery import Celery
from celery.task import periodic_task
from celery.schedules import crontab, solar

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)

app = Celery('celery_task', broker='redis://localhost:6379/0')


# My locations.
LATITUDE = 43.765204
LONGITUDE = -79.502520

# app.conf.beat_schedule = {
#     # Executes at sunset in Melbourne
#     'add-at-toronto-sunset': {
#         'task': 'celery_tasks.add',
#         'schedule': solar('sunrise', LATITUDE, LONGITUDE),
#         'args': (16, 16),
#     },
# }


@app.task(name='celery_tasks.add')
def add(x, y):
    total = x + y
    print(f'{x} + {y} = {total}')
    time.sleep(10)


@app.task(name='celery_tasks.test_post')
def test_post(x, y):
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

#TODO: Test soft time limit.
# @app.task(bind=True, max_retries=20, soft_time_limit=1)
# def data_extractor(self):
#     log.info(f"Running {self.name}.")
#     try:
#         for i in range(1, 11):
#             print('Crawling HTML DOM!')
#             if i == 5:
#                 raise ValueError('Crawling Index Error.')
#     except SoftTimeLimitExceeded:
#         print(f"Soft time limit exceeded for task: {self.name}.")
#     except Exception as exc:
#         print('There was an error let try after 5 seconds.')
#         log.exception(exc)
#         raise self.retry(exc=exc, countdown=backoff(self.request.retries))


# @periodic_task(bind=True, run_every=(crontab(minute='*/1')), ignore_result=True)
# def send_mail_queue(self):
#     try:
#         messages_sent = "example.email"
#         print(f"Task: {self.name}")
#         print(f"Total email message successfully sent {messages_sent}.")
#     finally:
#         print("release resources")
#
# key = '151361115230283ACB4F556778CBE87789100212620510281'
#
# @periodic_task(bind=True, run_every=timedelta(seconds=5), name='celery_task.send_mail_from_queue')
# def send_mail_from_queue(self):
#     REDIS_CLIENT = redis.Redis()
#     timeout = 60 * 5  # lock expires in 5 minutes
#     have_lock = False
#     my_lock = REDIS_CLIENT.lock(key, timeout=timeout)
#     try:
#         have_lock = my_lock.acquire(blocking=False)
#         if have_lock:
#             message = 'example.email'
#             print(f'{self.request.hostname}: Email Sent successfully, [{message}]')
#             time.sleep(10)
#     finally:
#         print('release resources')
#         if have_lock:
#             my_lock.release()



import time

from celery.result import AsyncResult

from celery_task import add

result = add.delay(2, 4)

while True:
    _result2 = AsyncResult(result.task_id)
    status = _result2.status
    print(status)
    if 'SUCCESS' in status:
        print(f'Result after 5 second wait {_result2.get()}')
        break
    time.sleep(5)

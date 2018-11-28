### Console scripts demonstrating python queue functionality.

#### Installation

```bash
$ make install
```

Running Simple python queue using threading library

```bash
$ conditional_task  # Runs a simple producer task with a single queue.
```

Running Celery tasks
====================

Install - Redis:

```bash
$ make redis-install 
```

##### Ensure redis is running
```bash
$ redis-cli ping
$ PONG
```

Start celery worker
```bash
$ celery -A celery_tasks worker --loglevel=info
```

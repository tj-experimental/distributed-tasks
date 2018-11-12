import threading
import queue

import time
import random

MAX_ITEMS = 10
QUEUE = queue.Queue(MAX_ITEMS)


class ProducerThread(threading.Thread):

    def run(self):
        numbers = range(MAX_ITEMS)
        global QUEUE

        while True:
            number = random.choice(numbers)
            QUEUE.put(number)
            print(f"Produced {number}")
            time.sleep(random.random())


class ConsumerThread(threading.Thread):

    def run(self):
        global QUEUE
        while True:
            number = QUEUE.get()
            QUEUE.task_done()
            print(f"Consumer 1: Consumed number {number}")
            time.sleep(random.random())


class Consumer2Thread(threading.Thread):

    def run(self):
        global QUEUE
        while True:
            number = QUEUE.get()
            QUEUE.task_done()
            print(f"Consumer 2: Consumed number {number}")
            time.sleep(random.random())


def main(*args):
    producer = ProducerThread()
    producer.start()

    consumer1 = ConsumerThread()
    consumer1.start()

    consumer2 = Consumer2Thread()
    consumer2.start()


if __name__ == '__main__':
    main()

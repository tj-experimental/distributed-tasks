import threading

import time
import random

QUEUE = []
MAX_ITEMS = 10

condition = threading.Condition()


class ProducerThread(threading.Thread):

    def run(self):
        numbers = range(MAX_ITEMS)
        global QUEUE

        while True:
            condition.acquire()

            if len(QUEUE) == MAX_ITEMS:
                print("Queue is full, producer is waiting")
                condition.wait()
                print("Space in queue, Consumer notified producer.")

            number = random.choice(numbers)
            QUEUE.append(number)
            print(f"Produced {number}")
            condition.notify()
            condition.release()
            time.sleep(random.random())


class ConsumerThread(threading.Thread):

    def run(self):
        global QUEUE
        while True:
            condition.acquire()
            if not QUEUE:
                print("Nothing in queue, consumer is waiting.")
                condition.wait()
                print("Producer added something to the queue and notify the consumer.")

            number = QUEUE.pop(0)
            print(f"Consumed number {number}")
            condition.notify()
            condition.release()
            time.sleep(random.random())



def main(*args):
    producer = ProducerThread()
    producer.start()

    consumer = ConsumerThread()
    consumer.start()

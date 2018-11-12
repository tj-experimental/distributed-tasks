import threading

counter_buffer = 0
counter_lock = threading.Lock()

consumer_max = 15

COUNTER_MAX = 1000000


def counter_consumer():
    global counter_buffer

    for i in range(COUNTER_MAX):
        counter_lock.acquire()
        counter_buffer += 1
        counter_lock.release()


def generate_consumer():
    consumers = []

    for i in range(consumer_max):
        con = threading.Thread(target=counter_consumer)
        consumers.append(con)

    return consumers


if __name__ == '__main__':
    consumers = generate_consumer()

    for con in consumers:
        con.start()

    for con in consumers:
        con.join()

    print(counter_buffer)

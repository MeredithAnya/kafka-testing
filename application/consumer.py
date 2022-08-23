from confluent_kafka import Consumer


from .bootstrap import bootstrap, TOPIC, CONSUMER_CONFIGURATION
c = Consumer(**CONSUMER_CONFIGURATION)

c.subscribe([TOPIC])

def consume() -> None:
    import time 
    start = time.time()

    interval = start + 10

    while True:
        if time.time() > interval:
            break
        msg = c.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        print('Received message: {}'.format(msg.value().decode('utf-8')))

    c.close()
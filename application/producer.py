from confluent_kafka import Producer

from .bootstrap import bootstrap, TOPIC, CONFIGURATION
from .messages import get_messages
p = Producer(**CONFIGURATION)




def callback(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]:{}'.format(msg.topic(), msg.partition(), msg.offset()))


def produce() -> None:
    for data in get_messages():
        p.poll(0)
        p.produce(TOPIC, data.encode('utf-8'), callback=callback)

    p.flush()
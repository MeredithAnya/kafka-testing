import logging
from syslog import LOG_CRIT
from typing import Optional, Sequence
from typing import MutableMapping, Union
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
import time
from pprint import pprint 

CONFIGURATION: MutableMapping [str, Union[str, int]] = {'bootstrap.servers': 'host.docker.internal:9092'}
CONSUMER_CONFIGURATION: MutableMapping [str, Union[str, int]]  = {**CONFIGURATION, 'group.id': 'mygroup','auto.offset.reset': 'earliest'}

TOPIC = "hackweek-topic-2"

def bootstrap() -> None:
    """
    Warning: Not intended to be used in production yet.
    """

    logger = logging.getLogger("test.bootstrap")


    config: MutableMapping [str, Union[str, int]]  = {**CONFIGURATION, "socket.timeout.ms": 1000, "debug": "broker,admin"}


    attempts = 0
    while True:
        try:
            print("Attempting to connect to Kafka (attempt %d)...", attempts)
            client = AdminClient(config)
            cluster_metadata = client.list_topics(timeout=1)
            pprint(cluster_metadata.topics)
            pprint(cluster_metadata.brokers)
            break
        except KafkaException as err:
            print(
                "Connection to Kafka failed (attempt %d)", attempts,
            )
            attempts += 1
            if attempts == 3:
                raise
            time.sleep(1)

    print("Connected to Kafka on attempt %d", attempts)

    print("Creating Kafka topics...")
    new_topic = NewTopic(TOPIC, num_partitions=16, replication_factor=1, config={})
    topics = client.create_topics([new_topic])

    try:
        topics[TOPIC].result(timeout=2)
        print("Topic %s created", TOPIC)
    except KafkaException as err:
        print("Failed to create topic %s",TOPIC)
        raise


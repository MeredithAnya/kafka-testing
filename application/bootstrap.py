import logging
from syslog import LOG_CRIT
from typing import Optional, Sequence
from typing import MutableMapping, Union
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
import time


CONFIGURATION: MutableMapping [str, Union[str, int]] = {'bootstrap.servers': '127.0.0.1:9092'}
CONSUMER_CONFIGURATION: MutableMapping [str, Union[str, int]]  = {**CONFIGURATION, 'group.id': 'mygroup','auto.offset.reset': 'earliest'}

TOPIC = "hackweek-topic"

def bootstrap() -> None:
    """
    Warning: Not intended to be used in production yet.
    """

    logger = logging.getLogger("test.bootstrap")


    config: MutableMapping [str, Union[str, int]]  = {**CONFIGURATION, "socket.timeout.ms": 1000}


    attempts = 0
    while True:
        try:
            logger.info("Attempting to connect to Kafka (attempt %d)...", attempts)
            client = AdminClient(config)
            client.list_topics(timeout=1)
            break
        except KafkaException as err:
            logger.debug(
                "Connection to Kafka failed (attempt %d)", attempts, exc_info=err
            )
            attempts += 1
            if attempts == 3:
                raise
            time.sleep(1)

    logger.info("Connected to Kafka on attempt %d", attempts)

    logger.info("Creating Kafka topics...")
    new_topic = NewTopic(TOPIC, num_partitions=16, replication_factor=1, config={})
    topics = client.create_topics([new_topic])

    try:
        topics[TOPIC].result()
        logger.info("Topic %s created", TOPIC)
    except KafkaException as err:
        logger.info("Failed to create topic %s",TOPIC , exc_info=err)


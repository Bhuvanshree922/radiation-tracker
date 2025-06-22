import time
import json
import pandas as pd
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
from constants import PLAYBACK_SPEED, SORT_COL, TOPIC

BOOTSTRAP_SERVERS = 'localhost:9092'
NUM_PARTITIONS = 3
REPLICATION_FACTOR = 1


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [Partition: {msg.partition()}]")


def ensure_topic_exists(topic_name, num_partitions, replication_factor):
    admin = AdminClient({'bootstrap.servers': BOOTSTRAP_SERVERS})
    topic_metadata = admin.list_topics(timeout=5)

    if topic_name in topic_metadata.topics:
        print(f"Topic '{topic_name}' already exists.")
        return

    new_topic = NewTopic(topic=topic_name,
                         num_partitions=num_partitions,
                         replication_factor=replication_factor)

    fs = admin.create_topics([new_topic])

    try:
        fs[topic_name].result()
        print(f"Topic '{topic_name}' created successfully.")
    except Exception as e:
        print(f"Failed to create topic '{topic_name}': {e}")
        raise


def get_producer():
    return Producer({
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'linger.ms': 1000,
        'acks': 'all'
    })


def send_producer(producer, chunk, playback_speed=PLAYBACK_SPEED):
    chunk[SORT_COL] = pd.to_datetime(chunk[SORT_COL], errors='coerce')
    chunk = chunk.dropna(subset=[SORT_COL])
    chunk['minute'] = chunk[SORT_COL].dt.floor('min')
    grouped = chunk.groupby('minute')
    last_group_time = None

    for group_time, group_rows in grouped:
        if last_group_time is not None:
            delay = (group_time - last_group_time).total_seconds() / playback_speed
            if delay > 0.01:
                time.sleep(delay)

        for _, row in group_rows.iterrows():
            safe_data = {
                k: (v.isoformat() if isinstance(v, pd.Timestamp)
                    else None if pd.isna(v)
                    else v)
                for k, v in row.drop('minute').to_dict().items()
            }

            producer.produce(
                topic=TOPIC,
                value=json.dumps(safe_data),
                callback=delivery_report
            )

        last_group_time = group_time

    producer.flush()
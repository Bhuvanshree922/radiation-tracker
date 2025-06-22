import pandas as pd
import pandas as pd
import time
from datetime import datetime
import json
from kafka import KafkaProducer
from kafka_helper import get_producer,send_producer,ensure_topic_exists
from constants import PLAYBACK_SPEED,TOPIC,REPLICATION_FACTOR,NUM_PARTITIONS

ensure_topic_exists(TOPIC, NUM_PARTITIONS, REPLICATION_FACTOR)
producer = get_producer()

df = pd.read_csv('/Users/bhuvanshree/ml/radiation_tracker/data/processed/fully_sorted.csv',chunksize=100000,on_bad_lines='skip')
for chunk in df:
    send_producer(producer,chunk,playback_speed=PLAYBACK_SPEED)

 
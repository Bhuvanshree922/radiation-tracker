import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

INPUT_CSV = os.path.join(BASE_DIR, 'data', 'measurements-out.csv')
SORTED_CHUNK_DIR = os.path.join(BASE_DIR, 'sorted_chunks')
FULLY_SORTED_CSV = 'fully_sorted.csv'
CHUNK_SIZE = 1_000_000
OUTPUT_FILE = os.path.join(BASE_DIR, 'data', 'fully_sorted.csv')

TOPIC = 'radiation-data-1'
SORT_COL = 'Captured Time'
PLAYBACK_SPEED = 60
NUM_PARTITIONS = 250
REPLICATION_FACTOR = 2

import pandas as pd
import os
from constants import CHUNK_SIZE,INPUT_CSV,SORTED_CHUNK_DIR

df = pd.read_csv(INPUT_CSV,chunksize=CHUNK_SIZE)
sum = 0
for i,chunk in enumerate(df):
    chunk = chunk.sort_values(by='Captured Time')
    os_path = os.path.join(SORTED_CHUNK_DIR,f'sorted_chunk{i}.csv')
    chunk.to_csv(os_path,index=False)


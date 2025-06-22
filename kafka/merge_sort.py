import pandas as pd
import glob
import csv
import heapq
from constants import SORTED_CHUNK_DIR, FULLY_SORTED_CSV

chunk_files = glob.glob(f"{SORTED_CHUNK_DIR}/*.csv")
file_reader = [open(file, 'r') for file in chunk_files]

headers = file_reader[0].readline().strip().split(',')
print(headers)

for f in file_reader[1:]:
    f.readline()

with open(FULLY_SORTED_CSV, 'w', newline='') as out_file:
    writer = csv.writer(out_file)
    writer.writerow(headers)

    heap = []


    for i, f in enumerate(file_reader):
        line = f.readline()
        if line:
            row = line.strip().split(',')
            heapq.heappush(heap, (row[0], i, row))


    while heap:
        timestamp, file_index, row = heapq.heappop(heap)
        writer.writerow(row)

        next_line = file_reader[file_index].readline()
        if next_line:
            next_row = next_line.strip().split(',')
            heapq.heappush(heap, (next_row[0], file_index, next_row))

for f in file_reader:
    f.close()

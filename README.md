# Radiation Tracker - Real-Time Radiation Monitoring Pipeline

This project simulates real-time radiation data streaming from a large historical dataset and processes it using **Apache Kafka** and **Apache Flink**. The final goal is to visualize radiation levels on a **world map dashboard**.

It is designed to handle **hundreds of millions of records** with a scalable Kafka setup (250 partitions), efficient pre-processing (external sorting), and stream processing using Flink.

---

## Tech Stack

- **Apache Kafka** – distributed messaging system for streaming data
- **Apache Flink** – stream processing engine (Java)
- **Python** – preprocessing and simulation scripts
- **Docker Compose** – orchestrates Kafka, Zookeeper, Flink
- **Safecast Radiation Dataset** – open data on global radiation levels

---

## Project Structure

```
radiation-tracker/
├── data/                         # Contains raw and processed datasets
├── kafka/                        # Kafka-related scripts and logic
│   ├── constants.py              # Config constants (paths, partitions, speed)
│   ├── kafka_helper.py          # Utilities for topic creation and producer
│   ├── producer.py              # Sends sorted CSV data to Kafka
│   ├── sort_data.py             # Splits and sorts large CSV in chunks
│   └── merge_sort.py            # Merges sorted chunks into a single CSV
├── sorted_chunks/               # Temporary sorted chunks directory
├── src/main/java/flink/         # Flink job (Java code)
│   └── KafkaOnlyJob.java
├── docker/                      # Docker configurations (optional)
├── docker-compose.yml           # Brings up Kafka + Flink cluster
├── Dockerfile                   # Flink job container build
└── README.md                    # This file
```

---

## Getting Started

### 1. Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Docker & Docker Compose
- Java 11+ and Apache Maven (for Flink job)
- Git

---

### 2. Clone the Repository

```bash
git clone https://github.com/Bhuvanshree922/radiation-tracker.git
cd radiation-tracker
```

---

### 3. Prepare the Dataset

1. Place the raw file `measurements.csv` in the `data/` folder.
2. Then, run the following preprocessing scripts:

```bash
# Step 1: Split and sort into chunks
python kafka/sort_data.py

# Step 2: Merge all sorted chunks into a final sorted CSV
python kafka/merge_sort.py
```

---

### 4. Start Kafka + Flink Cluster

Bring up Kafka, Zookeeper, and Flink JobManager/TaskManager:

```bash
docker-compose up --build
```

This will spin up the following services:
- Zookeeper
- Kafka broker
- Flink JobManager
- Flink TaskManager

---

### 5. Run the Kafka Producer (Python)

This script simulates real-time data streaming from the historical dataset:

```bash
python kafka/producer.py
```

The producer reads the `fully_sorted.csv` file and pushes records into Kafka at a configurable `PLAYBACK_SPEED`.

---

## Configuration Options

Edit the file: `kafka/constants.py`

```python
CHUNK_SIZE = 1_000_000                   # Rows per chunk during sort
PLAYBACK_SPEED = 60                     # Real-time simulation speed
TOPIC = 'radiation-data-1'              # Kafka topic
NUM_PARTITIONS = 250                    # Kafka partition count
REPLICATION_FACTOR = 2                  # Kafka replication
```

Use relative paths for portability (already handled in `constants.py`).

---

##  Flink Job

Flink job source: `src/main/java/flink/KafkaOnlyJob.java`

To build the Flink JAR:

```bash
cd src/main/java/flink
mvn clean package
```

Then submit the JAR to Flink UI (http://localhost:8081) or embed it into the Docker container.

---

##  Python Dependencies

Create a `venv` and install required libraries:

```bash
python -m venv venv
source venv/bin/activate
```

requirements

```
pandas
kafka-python
```

---

## 📚 Dataset Source

This project uses radiation data from the **Safecast** initiative:

- 🔗 https://safecast.org/

---

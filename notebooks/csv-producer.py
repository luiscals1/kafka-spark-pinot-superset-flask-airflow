# Event producer

import json
from sseclient import SSEClient as EventSource
from kafka import KafkaProducer

# Create producer

val spark = SparkSession
 .builder
 .appName("Spark-Kafka-Integration")
 .master("local")
 .getOrCreate()


producer = KafkaProducer(
    bootstrap_servers='kafka-server:29092', # kafka server ip address inspect - something like 172.23.0.5
    value_serializer=lambda v: json.dumps(v).encode('utf-8') #json serializer
    )

# Read streaming event
url = 'https://stream.wikimedia.org/v2/stream/recentchange'
try:
    for event in EventSource(url):
        if event.event == 'message':
            try:
                change = json.loads(event.data)
            except ValueError:
                pass
            else:
                #Send msg to topic wiki-changes
                producer.send('wiki-changes', change)

except KeyboardInterrupt:
    print("process interrupted")

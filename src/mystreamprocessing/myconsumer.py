from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'myoutputtopic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Reading messages from myoutputtopic:")
for message in consumer:
    print(f"Received: {message.value}")

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('myapptopic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest', 
    enable_auto_commit=True,
    group_id='myappconsumergroup',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')))

def consume_messages():
    for message in consumer:
        print(f"Received message: {message.value}")

if __name__ == "__main__":
    consume_messages()

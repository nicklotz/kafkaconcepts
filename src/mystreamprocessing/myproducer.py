from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_message(topic, message):
    producer.send(topic, value=message)
    producer.flush()
    print(f"Sent message: {message}")

if __name__ == "__main__":
    send_message('myinputtopic', 'This is an important message')
    send_message('myinputtopic', 'I love Kafka stream processing')
    send_message('myinputtopic', 'Another very important message')

from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092', 
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_message(topic, key, value):
    producer.send(topic, key=key.encode('utf-8'), value=value)
    producer.flush() 
    print(f"sent message to {topic}: {value}")

if __name__ == "__main__":
    name = input("Please enter your first name: ")
    numGreetings = int(input("Enter the number of greetings to send:" ))
    for i in range(numGreetings):
        message = {'number': i, 'name': name, 'message': f'This is greeting {i} to {name}'}
        send_message('myapptopic', f'key-{i}', message)
        time.sleep(1)

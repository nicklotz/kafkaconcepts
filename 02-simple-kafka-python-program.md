# 02: Writing a Simple Python App

## A. Python Prerequisites

1. Install **python** and **pip** if you don't have it already.
```
sudo apt update
sudo apt install -y python3 python3-pip
```

> [!NOTE]
> You can run `python --version` to check if Python is already installed.

2. Install the **kafka-python** library.
```
python3 -m pip install kafka-python
```

3. Start Kafka if it's not already running.
```
~/kafka_2.13-3.8.0/bin/kafka-server-start.sh -daemon config/server.properties
```

4. Create a new topic called **myapptopic**.
```
~/kafka_2.13-3.8.0/bin/kafka-topics.sh --create --topic myapptopic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

> [!NOTE]
> Kafka **topics** are information categories in Kafka. Each topic name is unique to a Kafka cluster. Producers send events to topics, and consumers read events from topics.

5. Verify the topic was successfully created.
```
~/kafka_2.13-3.8.0/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

## B. Write a Kafka producer and consumer

> A **producer** is an application that **publishes** Kafka events.

1. Create a directory called **mykafkapythonapp**.
```
mkdir ~/mykafkapythonapp
```
```
cd ~/mykafkapythonapp
```

2. Populate a file called **myproducer.py**.
```python
cat << EOF > myproducer.py
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
EOF
```

> A Kafka consumer is an application that reads and acts on Kafka events.

3. Populate a file called **myconsumer.py**.
```python
cat << EOF > myconsumer.py
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
EOF
```

## C. Test Event Handling

1. In one terminal screen, run the producer app. Enter your name and a positive integer when prompted.
```
python3 myproducer.py
``` 

2. In another terminal screen, run the consumer app.
```
python3 myconsumer.py
```

> What do the outputs of both the producer and consumer show?

## D. Cleaning Up

1. Stop the Kafka server
```
~/kafka_2.13-3.8.0/bin/kafka-server-stop.sh
```

2. Delete the Kafka topic if desired.
```
~/kafka_2.13-3.8.0/bin/kafka-topics.sh --delete --topic myapptopic --bootstrap-server localhost:9092
```

# 03: Streaming and Event Processing

> We will now implement software to perform stream processing on our Kafka events. We will use a library called **faust**, which is a Python fork of **Kafka streams**. 

## A. Install Faust

> We'll install the faust library using pip. It can also be added to your **requirements.txt**.

1. Install faust.
```
pip3 install faust-streaming
```

2. Verify the installation in your environment.
```
pip3 show faust-streaming
```

## B. Create Topics for Stream Processing

> Now we'll create two topics, an "input topic" for ingesting Kafka events, and an "output topic" for storing the results of the event processing.


1. Create a topic for ingesting data called **myinputtopic**.
```
kafka-topics.sh --create --topic myinputtopic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

2. Create a topic for handling processed data called **myoutputtopic**.
```
kafka-topics.sh --create --topic myoutputtopic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

3. Show the topics were successfully created.
```
kafka-topics.sh --list --bootstrap-server localhost:9092
```

## B. Create a Stream Processor for Stateless Data

1. Create a directory to hold our stream processing programs.
```
mkdir ~/mystreamprocessing
```
```
cd ~/mystreamprocessing
```

> We'll start by creating a simple program for handling statelesss messages. That is, messages that stand alone and don't depend on any previous or future data.

2. Populate a Python program called **mystatelessstreamprocessor.py**. 
```python
cat << EOF > mystatelessstreamprocessor.py
import faust

app = faust.App(
    'mystatelessstreamprocessor',
    broker='kafka://localhost:9092',
    store='memory://'
)

myinputtopic = app.topic('myinputtopic', value_type=str)
myoutputtopic = app.topic('myoutputtopic', value_type=str)

@app.agent(myinputtopic)
async def process(stream):
    async for message in stream:
        if 'important' in message:
            # Send the message to myoutputtopic if the string 'important' is in message
            await myoutputtopic.send(value=f"Processed: {message}")
            print(f"Processed message: {message}")

if __name__ == '__main__':
    app.main()
EOF
```

## C. Create a Stream Porcessor for Stateful Data

> Next, we'll create a processor for maintaining state between messages. A simple example is counting how many times a particular string occurs in the stream.

1. Populate a Python program called **mystatefulstreamprocessor.py**.

```python
cat << EOF > mystatefulstreamprocessor.py
import faust

app = faust.App(
    'mystatefulstreamprocessor',
    broker='kafka://localhost:9092',
    store='memory://'
)

myinputtopic = app.topic('myinputtopic', value_type=str)
myoutputtopic = app.topic('myoutputtopic', value_type=str)

wordcount_table = app.Table('wordcounts', default=int)

@app.agent(myinputtopic)
async def count_words(stream):
    async for message in stream:
        words = message.split()
        for word in words:
            wordcount_table[word] += 1
            await myoutputtopic.send(value=f"{word}: {wordcount_table[word]}")
            print(f"Count for {word}: {wordcount_table[word]}")

if __name__ == '__main__':
    app.main()
EOF
```

## D. Create Kafka Producer

> This next program is a Kafka producer needed to send messages to our input topic.

1. Populate a Python program called **myproducer.py**.
```python
cat << EOF > myproducer.py
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
EOF
```

2. Run the producer program.
```
python3 myproducer.py
```

## E. Test Stream Processing.

1. Run the stateless stream processor.
```
python3 mystatelessstreamprocessor.py
```

2. Run the stateful stream processor.
```
python3 mystatefulstreamprocessor.py
```

## F. Create a Kafka Consumer to Read from the Output Topic

1. Populate a Python program called **myconsumer.py**.
```python
cat << EOF > myconsumer.py
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
EOF
```

2. Run the consumer program.
```
python3 myconsumer.py
```

## G. Clean Up

1. If desired, delete the Kafka topics created.
```
kafka-topics.sh --delete --topic myinputtopic --bootstrap-server localhost:9092
```
```
kafka-topics.sh --delete --topic myoutputtopic --bootstrap-server localhost:9092
```


















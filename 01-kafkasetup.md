# 01: Install and Set Up Apache Kafka

> [!IMPORTANT]  
> These steps assume a Debian Linux host. The commands shown below may differ if you are using a different Linux distro, or are running on MacOS or Windows.

## A. Install Kafka

1. Download the Kafka tarball from Apache.
```
curl https://dlcdn.apache.org/kafka/3.8.0/kafka_2.13-3.8.0.tgz  -o kafka_2.13-3.8.0.tgz
```

2. Extract the archive.
```
tar -xzf kafka_2.13-3.8.0.tgz
```
```
cd kafka_2.13-3.8.0
```

3. Install Java if needed.
```
sudo apt-get install -y openjdk-17-jdk
```

> [!IMPORTANT]
> Java is required to install and use Apache Kafka.

4. Generate and store a unique cluster ID using the provided shell script.
```
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
```
```
echo $KAFKA_CLUSTER_ID
```

5. Format and verify Kafka logging directories.
```
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties
```

6. Start the Kafka server in the background.
```
bin/kafka-server-start.sh -daemon config/kraft/server.properties
```

7. If desied, stop the Kafka server.
```
/bin/kafka-server-stop.sh
```

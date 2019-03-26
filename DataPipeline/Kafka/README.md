# Test streaming twitter data and storing them in Kafka using the topic 'tweets'

Steps:
1. Get twitter creds (either get file from me or get your own)
2. Install binary of Kafka version 2.12-2.1.0
3. runs these commands if not already installed (pip install kafka-python, pip install python-twitter, pip install tweepy)
4. Put twitter_creds.txt in same directory as TwitterStreaming.py
5. Runs these commands in seperate terminals in order from the kafka_2.12-2.1.0 directory
	- bin/zookeeper-server-start.sh config/zookeeper.properties
	- bin/kafka-server-start.sh config/server.properties
	- bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic tweets (if not already created)
	- python2 KafkaProducer.py
       - python2 KafkaConsumer

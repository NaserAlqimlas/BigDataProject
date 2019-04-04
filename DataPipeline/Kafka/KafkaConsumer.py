from kafka import KafkaConsumer, KafkaClient
from pymongo import MongoClient
import dns
import json


consumer = KafkaConsumer(
    'tweets',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group')

#add tweets from US to mongoDB server on GCP
client = MongoClient("mongodb://104.197.54.204",27017)
collection = client.tweets.tweet
for message in consumer:
	message = message.value
	tweet = json.loads(message)
	collection.insert_one(tweet)
	print('{} added to {}'.format(message, collection))
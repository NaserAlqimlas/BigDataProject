'''
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient
with open("twitter_creds.txt") as f:
    content = f.readlines()
content = [x.strip() for x in content]
ACCESS_TOKEN = content[0]
ACCESS_SECRET = content[1]
CONSUMER_KEY = content[2]
CONSUMER_SECRET = content[3]
class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages("tweets", data.encode('utf-8'))
        #print (data)
        return True
    def on_error(self, status):
        print (status)
kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)
l = StdOutListener()
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
stream = Stream(auth, l)
stream.filter(track=["a", "I", "the", "be", "to", "of", "and", "in", "that", "have"])
'''
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient
import ConfigParser

# with open("twitter_creds.txt") as f:
#     content = f.readlines()
# content = [x.strip() for x in content]
#
# ACCESS_TOKEN = content[0]
# ACCESS_SECRET = content[1]
# CONSUMER_KEY = content[2]
# CONSUMER_SECRET = content[3]
cf = ConfigParser.ConfigParser()
cf.read("twitter_conf.conf")
ACCESS_TOKEN=cf.get("develop", "ACCESS_TOKEN")
ACCESS_SECRET=cf.get("develop", "ACCESS_SECRET")
CONSUMER_KEY=cf.get("develop", "CONSUMER_KEY")
CONSUMER_SECRET=cf.get("develop", "CONSUMER_SECRET")

class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages("test", data.encode('utf-8'))
        print (data)
        return True
    def on_error(self, status):
        print (status)
        return True

kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)
l = StdOutListener()
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
stream = Stream(auth, l)
stream.filter(locations = [-124.7771694, 24.520833, -66.947028, 49.384472])

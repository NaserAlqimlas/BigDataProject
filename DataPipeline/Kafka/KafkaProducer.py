from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient
from tweepy import API

class StdOutListener(StreamListener):
	def __init__(self,api):
		self.api = api
		super(StreamListener, self).__init__()
		kafka = KafkaClient("localhost:9092")
		self.producer = SimpleProducer(kafka)
	def on_data(self, data):
		self.producer.send_messages("tweets", data.encode('utf-8'))
		print (data)
		return True
	def on_error(self, status):
		print (status)

if __name__ == '__main__':
	with open("twitter_creds.txt") as f:
		content = f.readlines()
		content = [x.strip() for x in content]


	ACCESS_TOKEN = content[0]
	ACCESS_SECRET = content[1]
	CONSUMER_KEY = content[2]
	CONSUMER_SECRET = content[3]
	auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
	api = API(auth)
	l = StdOutListener(api)
	
	
	stream = Stream(auth, l)
	stream.filter(locations=[-180,-90,180,90],languages=['en'])

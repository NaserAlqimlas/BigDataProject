from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient


class StdOutListener(StreamListener):
	def __init__(self,api):
		self.api = api
		super(StreamListener, self).__init__()
		kafka = KafkaClient("localhost:9092")
		self.producer = SimpleProducer(kafka)


    def on_data(self, data):
        producer.send_messages("tweets", data.encode('utf-8'))
        #print (data)
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

	l = StdOutListener()
	auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
	api = API(auth)
	stream = Stream(auth, l)
	stream.filter(locations=[-180,-90,180,90],lang=['en'])

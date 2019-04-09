import pyspark
from pyspark.sql import SparkSession
import pymongo
import json
import copy
from pyspark.sql.functions import lower, col
from pyspark import SparkContext
import pyspark.sql 


my_spark = SparkSession \
    .builder \
    .appName("myApp") \
    .master("local[4]") \
    .config("spark.mongodb.input.uri", "mongodb://104.197.54.204/tweets.tweet") \
    .config("spark.mongodb.output.uri", "mongodb://104.197.54.204/tweets.words") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.11:2.4.0") \
    .getOrCreate()

if __name__ == "__main__":

	#spark = SparkSession.builder.appName("test").getOrCreate()

	df = my_spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
	# df.show()
	#df.collect()
	# rx = ".*"+keyword+".*"
	#text = df.text

	#lower case all tweets
	unionDF = df.select(df.text)
	unionDF = unionDF.withColumn('text', lower(col('text')));

	#get keyword
	#trump: 1938
	keyword = "trump"
	tweets_with_words = unionDF[unionDF['text'].contains(keyword)]
	# tweets_with_words = unionDF.filter(unionDF.text == keyword)

	count = tweets_with_words.count()
	# Tokens = unionDF.select("trump").collect();
	# tweets_with_words = unionDF.filter(unionDF.text[keyword])
	
	#new_rdd = rdd.filter(lambda x: x in Tokens)
	full_name = "county, State"
	
	print(count)
	# print(tweets_with_words)
	tweets_with_words.select("text").show(10)
	print(tweets_with_words.head(10))
	# unionDF.show()

	# print(unionDF.head(100))






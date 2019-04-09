import pyspark
from pyspark.sql import SparkSession
import pymongo
import json
import copy
from pyspark.sql.functions import lower, col
from pyspark import SparkContext
import pyspark.sql 
from pyspark.sql.functions import explode


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
	unionDF = df.select(df.text, df.place)
	unionDF = unionDF.withColumn('text', lower(col('text')));
	explode_DF = unionDF.withColumn('place', explode('full_name'))
	#get keyword
	#trump: 1938
	keyword = "trump"
	tweets_with_words = unionDF[unionDF['text'].contains(keyword)]
	# tweets_with_words = unionDF.filter(unionDF.text == keyword)

	count = tweets_with_words.count()
	# Tokens = unionDF.select("trump").collect();
	# tweets_with_words = unionDF.filter(unionDF.text[keyword])
	
	#new_rdd = rdd.filter(lambda x: x in Tokens)
	'''
	full_name = "county, State"
	'''

	print(count)
	print(explode_DF.head(2))
	tweets_with_words.select("text").show(10)
	print(tweets_with_words.head(10))

	states = {
        'AK': 0,
        'AL': 0,
        'AR': 0,
        'AZ': 0,
        'CA': 0,
        'CO': 0,
        'CT': 0,
        'DE': 0,
        'FL': 0,
        'GA': 0,
        'GU': 0,
        'HI': 0,
        'IA': 0,
        'ID': 0,
        'IL': 0,
        'IN': 0,
        'KS': 0,
        'KY': 0,
        'LA': 0,
        'MA': 0,
        'MD': 0,
        'ME': 0,
        'MI': 0,
        'MN': 0,
        'MO': 0,
        'MS': 0,
        'MT': 0,
        'NC': 0,
        'ND': 0,
        'NE': 0,
        'NH': 0,
        'NJ': 0,
        'NM': 0,
        'NV': 0,
        'NY': 0,
        'OH': 0,
        'OK': 0,
        'OR': 0,
        'PA': 0,
        'RI': 0,
        'SC': 0,
        'SD': 0,
        'TN': 0,
        'TX': 0,
        'UT': 0,
        'VA': 0,
        'VT': 0,
        'WA': 0,
        'WI': 0,
        'WV': 0,
        'WY': 0
	}


	# unionDF.show()

	# print(unionDF.head(100))






import pyspark
from pyspark.sql import SparkSession
import pymongo
import json
import copy
from pyspark.sql.functions import lower, col
from pyspark import SparkContext
import pyspark.sql
from pyspark.sql.functions import explode
import sys


conf = pyspark.SparkConf()
#conf.setMaster("spark://104.198.99.155.80:7077")
conf.set("spark.mongodb.input.uri", "mongodb://104.197.54.204/tweets.tweet")
conf.set("spark.mongodb.output.uri", "mongodb://104.197.54.204/tweets.words")
conf.set("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.11:2.3.2")
sc = pyspark.SparkContext(conf=conf)
my_spark = SparkSession(sc)

'''
my_spark = SparkSession \
    .builder \
    .appName("myApp") \
    .master("spark://35.233.240.80:8088") \
    .config("spark.mongodb.input.uri", "mongodb://104.197.54.204/tweets.tweet") \
    .config("spark.mongodb.output.uri", "mongodb://104.197.54.204/tweets.words") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.11:2.3.2") \
    .getOrCreate()
'''

if __name__ == "__main__":
    print("Hello World")

    #spark = SparkSession.builder.appName("test").getOrCreate()

    df = my_spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
    # df.show()
    #df.collect()
    # rx = ".*"+keyword+".*"
    #text = df.text

    #lower case all tweets
    unionDF = df.select(df.text, df.place)
    unionDF = unionDF.withColumn('text', lower(col('text')));
    # explode_DF = unionDF.withColumn('full_name', explode('full_name'))
    #get keyword
    #trump: 1938
    keyword = sys.argv[1].lower()
    tweets_with_words = unionDF[unionDF['text'].contains(keyword)]
    df2 = tweets_with_words.select('text', "place.*")
    #df2.printSchema()
    # tweets_with_words = unionDF.filter(unionDF.text == keyword)

    #count = tweets_with_words.count()
    # Tokens = unionDF.select("trump").collect();
    # tweets_with_words = unionDF.filter(unionDF.text[keyword])

    #new_rdd = rdd.filter(lambda x: x in Tokens)
    '''
    full_name = "county, State"
    '''

    #print(count)
    #print(unionDF.head(2))
    #print(tweets_with_words.head(2))
    #tweets_with_words.select("text").show(10)
    # print(tweets_with_words.head(10))

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

    us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI', #['Michigan', ' USA']
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

    places = df2.select("full_name").collect()
    #print(len(places))
    l = []
    for i in range(len(places)):
        l.append(places[i].__getitem__("full_name"))


    state = us_state_abbrev.keys()
    abbr = states.keys()

    for i in l:
        if(i == None):
            continue
        l2 = i.split(',')
        if len(l2) == 1 or len(l2) > 2:
            continue
        l2[0] = l2[0].replace(" ", "")
        l2[1] = l2[1].replace(" ", "")
        if(l2[1] == 'USA'):
            if(l2[0] in state):
                a = us_state_abbrev[l2[0]]
                states[a] += 1
            else:
                continue
        else:
            if(l2[1] in abbr):
                states[l2[1]] += 1
            else:
                continue

    states['word'] = keyword
    client = pymongo.MongoClient("mongodb://104.197.54.204",27017)
    db = client["tweets"]
    coll = db['words']
    coll.update_one({'word': keyword}, {"$set": states}, upsert=True)
    #print(states)

import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import ast
import json
#import pymongo_spark
# Important: activate pymongo_spark.
#pymongo_spark.activate()

brokers, topic = 'localhost:9092', 'test'
print("**************************************")
if __name__ == "__main__":
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
    sc = SparkContext(appName="PythonStreamingDirectKafkaWordCount")
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, 5)

    statesContext = sc.broadcast(states)
    abbrevContext = sc.broadcast(us_state_abbrev)

    kvs = KafkaUtils.createDirectStream(ssc, [topic],{"metadata.broker.list": brokers})

    def foo(x):
        print(json.loads(x[1])[u'user'])
        if("location" not in json.loads(x[1])[u'user']):
            print("No")
            return "No"
        location = json.loads(x[1])[u'user'].get('location')
        #can not print, there are characters encoded wrong
        #print(location)

        if location != None:
            print(statesContext.value)
            words = location.split(", ")
            print(words)
            for w in words:
                if w.upper() in statesContext.value.keys():
                    print(w.upper())
                    return w.upper()
                w2 = w.split(" ")
                for e in w2:
                    if e in abbrevContext.value.keys():
                        print(abbrevContext.value[e])
                        return abbrevContext.value[e]
            print("No")
            return "No"
        print("No")
        return "No"


    lines = kvs.map(lambda x: foo(x))
    print("finish map!")
    #fliter_lines = lines.map(lambda x: filter_location(x))

    lines_filter = lines.filter(lambda x: x != "No")
    counts = lines_filter.flatMap(lambda line:line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a+b)


    print('*****************')
    counts.pprint()
    print('*****************')

    ssc.start()
    ssc.awaitTermination()

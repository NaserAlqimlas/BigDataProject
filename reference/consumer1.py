import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import ast
import json

brokers, topic = 'localhost:9092', 'test'
print("**************************************")
if __name__ == "__main__":
    sc = SparkContext(appName="PythonStreamingDirectKafkaWordCount")
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, 5)
    kvs = KafkaUtils.createDirectStream(ssc, [topic],{"metadata.broker.list": brokers})
    def foo(x):
        print(json.loads(x[1])[u'user'])
        print(json.loads(x[1])[u'user'].get('location',"null"))
        return json.loads(x[1])[u'user'].get('location',"null")
              
    lines = kvs.map(lambda x: foo(x))
    counts = lines.flatMap(lambda line:line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a+b)
    print('*****************')
    counts.pprint()
    print('*****************')
    ssc.start()
    ssc.awaitTermination()

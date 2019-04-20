import subprocess
import sys

if __name__ == '__main__':
	keyword = sys.argv[1]
	subprocess.call("spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.1.0.jar KafkaConsumer.py "+ keyword, shell=True)

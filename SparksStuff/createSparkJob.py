import subprocess
import sys

if __name__ == '__main__':
	keyword = sys.argv[1]
	subprocess.call('gcloud dataproc jobs submit pyspark --cluster=cluster-56f5 --region=us-west1 data_processing.py -- ' + keyword, shell=True)
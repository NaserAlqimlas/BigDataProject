#!/bin/bash

#run this file on a google cloud dataproc server to set up the reqired environment
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

sudo python get-pip.py

sudo pip install pymongo

wget http://central.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.11/2.3.2/
mongo-spark-connector_2.11-2.3.2.jar

wget http://central.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.11/2.3.2/
mongo-spark-connector_2.11-2.3.2.jar

sudo cp mongo-spark-connector_2.11-2.3.2.jar /usr/lib/spark/jars

wget http://central.maven.org/maven2/org/mongodb/mongo-java-driver/3.8.1/mongo-java-driv
er-3.8.1.jar

sudo cp mongo-java-driver-3.8.1.jar /usr/lib/spark/jars
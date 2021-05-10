import codecs
import json
import re
from datetime import datetime

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

from mongo_db_store import MongoDBStore
from covid_data_collector import CovidDataCollector
from data_stream_provider import DataStreamProvider
from data_store_provider import DataStoreProvider


def applyTransformation(data, isFilter, filterStrings):
    """ Apply filtering & transfomration according to the configuration"""
    if isFilter:
        for filterString in filterStrings:
            filterString = filterString.replace("\\\\", "\\")
            data = re.sub(filterString, '', data, flags=re.MULTILINE)
    return data


def getStore(output):
    """Get store based on Output"""
    return DataStoreProvider().getStore(output)


def getCovidInputObject(covidInput):
    return CovidDataCollector(covidInput["url"])


def storeData(rdd, fieldName, outputs, covidInputObj, covidInputFieldName):
    input = rdd.collect()
    print(input)
    for output in outputs:
        outputStore = getStore(output)
        if outputStore is None:
            print("Data store not present for " + output["name"])
        json_data_file = {}
        json_data_file[fieldName] = input
        json_data_file['timestamp'] = datetime.now()
        json_data_file[covidInputFieldName] = covidInputObj.getData()
        outputStore.save(output["schema_name"], output["table_name"], json_data_file)


def getStream(input):
    return dataStreamProvider.getStream(ssc, input)


# Fetch Configuration
with open("config.json") as json_data_file:
    data = json.load(json_data_file)

# Get Inputs and Ouputs
inputs = data["inputs"]
outputs = data['outputs']
covidInput = data['covid_input']
covidInputObj = getCovidInputObject(covidInput)
# Set up the Spark context and the streaming context
sc = SparkContext(appName=data['app_name'])
ssc = StreamingContext(sc,data['batch_duration'])
dataStreamProvider = DataStreamProvider()
dataStoreProvider = DataStoreProvider()

# For each input process the data in stream
for input in inputs:
    recordsDStream = getStream(input)
    # If no Valid DatastreamProvider Present to be connected
    if recordsDStream == None:
        print("No Valid Stream present for connection")
        exit(1)

    transformedDStream = recordsDStream.map(
        lambda data: applyTransformation(data, input["filtering"], input["filter_strings"]))
    transformedDStream.foreachRDD(
        lambda rdd: storeData(rdd, input["output_field"], outputs, covidInputObj, covidInput['output_field']))

ssc.start()
ssc.awaitTermination()

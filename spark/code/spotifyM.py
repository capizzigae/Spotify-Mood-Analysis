from os import name
from pyspark.sql.session import SparkSession
from pyspark.streaming import StreamingContext
import pyspark
from pyspark.sql import SparkSession
import pyspark.sql.types as tp
from pyspark.sql import Row
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.feature import IndexToString, StringIndexer
from elasticsearch import Elasticsearch
import json
from typing import Optional
from pyspark import SparkContext
from pyspark.conf import SparkConf
from pyspark.sql.functions import from_json, struct, to_json
from pyspark.sql.dataframe import DataFrame

sc = SparkContext(appName="spotifyMoodAnalysis")
spark = SparkSession(sc)
sc.setLogLevel("WARN")

elastic_host="172.18.0.51"
elastic_index="spotify"
elastic_document="_doc"

#training classification model
file="../tap/spark/dataset/songs_training_set.csv"
schema= tp.StructType([
    #tp.StructField(name= 'id', dataType=tp.IntegerType(), nullable=True),
    tp.StructField(name= 'Artist', dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'Song', dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'uri', dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'Acousticness', dataType= tp.FloatType(),  nullable= True),
    tp.StructField(name= 'Danceability', dataType= tp.FloatType(),  nullable= True),
    tp.StructField(name= 'Liveness', dataType= tp.FloatType(),  nullable= True),
    tp.StructField(name= 'Loudness', dataType= tp.FloatType(),  nullable= True),
    tp.StructField(name= 'Speechiness', dataType= tp.FloatType(),  nullable= True),
    tp.StructField(name= 'label', dataType= tp.IntegerType(),  nullable= True),
])

trainingset= spark.read.csv(file,header=True,schema=schema)

assembler=VectorAssembler(inputCols=["Acousticness","Danceability","Liveness","Loudness","Speechiness"],outputCol="features")
#indexer=StringIndexer(inputCol="Classification",outputCol="labelIndex").fit(trainingset)
regression=LogisticRegression(maxIter=10, featuresCol='features')
stringer = IndexToString(inputCol="prediction", outputCol="predictionString", labels=['Melancholic','Energetic','Groovy','Chill'])
pipeline=Pipeline(stages=[assembler,regression,stringer])
pipelineFit= pipeline.fit(trainingset)

#to try with the load if i have time
#pipelineFit.save("../tap/spark/dataset/model.save")

#mapping for elasticSearch
es_mapping = {
    "mappings": {
        "properties": 
            {
                "Song": {"type": "text","fielddata": True},
                "Artist": {"type": "text","fielddata": True},
                "uri": {"type": "text","fielddata": True},
                "@timestamp": {"type": "date","format": "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'"}
            }
    }
}

#Connecting and create index

es = Elasticsearch(hosts=elastic_host) 

response = es.indices.create(
    index=elastic_index,
    body=es_mapping,
    ignore=400 # ignore 400 already exists code
)

if 'acknowledged' in response:
    if response['acknowledged'] == True:
        print ("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])



#Processing songs
kafkaServer="172.18.0.23:9092"
topic = "sp"

conf = SparkConf(loadDefaults=False)

songKafka = tp.StructType([
    #tp.StructField(name= 'id', dataType=tp.IntegerType(), nullable=True),
    tp.StructField(name= 'Artist', dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'Song', dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'uri', dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'Acousticness', dataType= tp.FloatType(),  nullable= True),
    tp.StructField(name= 'Danceability', dataType= tp.FloatType(),  nullable= True),
    tp.StructField(name= 'Liveness', dataType= tp.FloatType(),  nullable= True),
    tp.StructField(name= 'Loudness', dataType= tp.FloatType(),  nullable= True),
    tp.StructField(name= 'Speechiness', dataType= tp.FloatType(),  nullable= True),
    tp.StructField(name= '@timestamp', dataType= tp.StringType(),  nullable= True)
])

def elaborate(batch_df: DataFrame, batch_id: int):
    batch_df.show(truncate=False)
    if not batch_df.rdd.isEmpty():
        print("********************")
        data2=pipelineFit.transform(batch_df)
        data2.show()

        data2.select("Song", "Artist","uri","@timestamp","predictionString") \
        .write \
        .format("org.elasticsearch.spark.sql") \
        .mode('append') \
        .option("es.mapping.id","uri") \
        .option("es.nodes", elastic_host).save(elastic_index)


df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", kafkaServer) \
  .option("subscribe", topic) \
  .load()

df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", songKafka).alias("data")) \
    .select("data.*") \
    .writeStream \
    .foreachBatch(elaborate) \
    .start() \
    .awaitTermination()


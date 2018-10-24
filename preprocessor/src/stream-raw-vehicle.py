from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, split, get_json_object
from pyspark.sql.types import *
import os

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.2 ' \
                                    'pyspark-shell'

vehicleschema = StructType([StructField("event_id", IntegerType(), True),
                            StructField("vehicle_id", IntegerType(), True),
                            StructField("vehicle_speed", FloatType(), True),
                            StructField("engine_speed", IntegerType(), True),
                            StructField("tire_pressure", IntegerType(), True),
                            StructField("location", ArrayType(
                                StructType([
                                    StructField("latitude", FloatType()),
                                    StructField("longitude", FloatType())
                                ]

                                )
                            ), True)])

spark = SparkSession \
    .builder \
    .appName("Streaming vehicle Data") \
    .getOrCreate()
print(spark.conf.get)
# org.apache.spark.sql.kafka010.KafkaSourceProvider
dfraw = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:29092") \
    .option("subscribe", "vehicle-topic") \
    .load()

# .schema(spark.read.json("vehicle-schema")) \

dfraw.printSchema()
df = dfraw.select("value", from_json(dfraw["value"].cast("string"), vehicleschema).alias("value"))
##df = dfraw.selectExpr("CAST(value AS STRING)")

# print(type(dfraw))
# print(type(df))
##split_col = split(df['value'], ';')

##df = df.withColumn('jsonval', split_col.getItem(0)).drop('value').drop('value')
# .select(from_json('jsonval', schema_data.replace('\n', '')))

# json_schema = spark.read.json(parseddf.rdd.map(lambda r: r.json)).schema

# spark.read.json(df.rdd.map(lambda r: r.json))
# new_df = df.select(get_json_object(df['jsonval'], '$.direction').alias('direction'),
#                    get_json_object(df['jsonval'], '$.event_id').alias('event_id'),
#                    get_json_object(df['jsonval'], '$.vehicle_id').alias('vehicle_id'),
#                    get_json_object(df['jsonval'], '$.engine_speed').alias('engine_speed'),
#                    get_json_object(df['jsonval'], '$.tire_pressure').alias('tire_pressure'))

# dfrawQuery = dfraw \
#     .writeStream \
#     .queryName("qdfraw") \
#     .format("console") \
#     .start()
#
# dfQuery = df \*
#     .writeStream \
#     .queryName("qdf") \
#     .format("console") \
#     .option('truncate', 'false') \
#     .start()

new_dfQuery = df \
    .writeStream \
    .queryName("qnew_df") \
    .format("console") \
    .option('truncate', 'false') \
    .start().awaitTermination()

esQuery = df \
    .writeStream \
    .outputMode("append") \
    .queryName("qes") \
    .format("org.elasticsearch.spark.sql") \
    .option("es.nodes", "127.0.0.1") \
    .option("es.port", "9200") \
    .option("es.index.auto.create", "true") \
    .option("checkpointLocation", "/tmp/stream1_checkpoint") \
    .start("transport/cars").awaitTermination()  # index/docType
# .option("es.resource.auto.create", "transport/cars") \

spark.streams.awaitAnyTermination()

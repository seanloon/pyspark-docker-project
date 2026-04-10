from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .config("spark.eventLog.enabled", "true") \
    .config("spark.eventLog.dir", "/spark-events") \
    .getOrCreate()
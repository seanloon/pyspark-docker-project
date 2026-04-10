from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("TestApp").getOrCreate()
df = spark.range(10)
df.show()
spark.stop()
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit

spark = SparkSession.builder.getOrCreate()

data = [("Alice", 10), ("Bob", 20)]
df = spark.createDataFrame(data, ["name", "score"])

# Add a constant column
df_with_constant = df.withColumn("bonus", lit(5))

# Use lit in an expression
df_with_total = df.withColumn("total", col("score") + lit(5))

print("Show df_with_constant")
df_with_constant.show()
print ("Show df_with_total")
df_with_total.show()

print("Show df")
df.withColumn("total", col("score") + lit(5)).show()

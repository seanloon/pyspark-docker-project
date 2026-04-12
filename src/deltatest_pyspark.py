from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp
from pyspark.sql.types import StructType, StructField, IntegerType
from delta.tables import DeltaTable
from delta.pip_utils import configure_spark_with_delta_pip

spark = configure_spark_with_delta_pip(SparkSession.builder \
    .appName("DeltaTest") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")).getOrCreate()

# Create a DataFrame with some sample data
data = [(101, 500), (102, 2000), (103, 900)]
schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("revenue", IntegerType(), True)])


source_df = spark.createDataFrame(data, schema)

# Create a target DataFrame with the same schema
target_data = [(101, 450), (102, 100)]
target_df = spark.createDataFrame(target_data, schema)


if DeltaTable.isDeltaTable(spark, "/gold/orders_enriched"):
    dt = DeltaTable.forPath(spark, "/gold/orders_enriched")
    t = dt.alias("t")
    s = source_df.alias("s")
    
    t.merge(
        s, col("t.order_id") == col("s.order_id"))\
        .whenMatchedUpdate(set={"revenue": col("s.revenue"), "last_updated": current_timestamp()})\
        .whenNotMatchedInsert(values={"order_id": col("s.order_id"), "revenue": col("s.revenue"), "last_updated": current_timestamp()})\
        .execute()
    
    print("Merged DataFrame:")
    dt.toDF().show()
else:
    print("Path /gold/orders_enriched is not a Delta table")
    print("Creating sample Delta table for demonstration...")
    
    # Create a simple Delta table for testing
    target_df.write.format("delta").mode("overwrite").save("/tmp/test_delta")
    dt = DeltaTable.forPath(spark, "/tmp/test_delta")
    print("Sample Delta table created:")
    dt.toDF().show()
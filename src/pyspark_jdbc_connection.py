from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ReadDbTable").getOrCreate()

jdbc_url = "jdbc:postgresql://db-host:5432/my_database"
table_name = "schema.table_x"
properties = {
    "user": "my_user",
    "password": "my_password",
    "driver": "org.postgresql.Driver"
}

df = spark.read.jdbc(url=jdbc_url, table=table_name, properties=properties)
df.createOrReplaceTempView("table_x")

spark.sql("SELECT * FROM table_x").show()

spark.stop()
'''
$env:DB_HOST = "your-db-host"
$env:DB_PORT = "5432"
$env:DB_NAME = "your-database"
$env:DB_USER = "your-user"
$env:DB_PASSWORD = "your-password"
python src\pyspark_jdbc_connection.py
'''

import os
from pyspark.sql import SparkSession

# Load credentials from environment variables (not hardcoded)
db_host = os.getenv("DB_HOST", "db-host")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "my_database")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

if not db_user or not db_password:
    raise ValueError("DB_USER and DB_PASSWORD environment variables must be set")

# Initialize Spark with optimized settings
spark = SparkSession.builder \
    .appName("ReadDbTable") \
    .getOrCreate()

try:
    # Build JDBC URL and properties
    jdbc_url = f"jdbc:postgresql://{db_host}:{db_port}/{db_name}"
    table_name = "schema.table_x"
    properties = {
        "user": db_user,
        "password": db_password,
        "driver": "org.postgresql.Driver",
        "fetchsize": "10000"
    }

    # Read from database with error handling
    df = spark.read.jdbc(url=jdbc_url, table=table_name, properties=properties)
    print(f"Successfully loaded {df.count()} rows from {table_name}")
    
    df.createOrReplaceTempView("table_x")
    spark.sql("SELECT * FROM table_x LIMIT 10").show()

except Exception as e:
    print(f"Error reading from database: {e}")
    raise

finally:
    # Always stop Spark session
    spark.stop()
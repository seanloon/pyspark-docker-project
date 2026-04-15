from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder.appName("SelectTableX").getOrCreate()

    # Sample data for table_x; replace this with a real table source as needed.
    data = [
        (1, "Alice"),
        (2, "Bob"),
        (3, "Charlie")
    ]
    columns = ["id", "name"]

    df = spark.createDataFrame(data, columns)
    df.createOrReplaceTempView("table_x")

    result = spark.sql("SELECT * FROM table_x")
    result.show()

    spark.stop()


if __name__ == "__main__":
    main()

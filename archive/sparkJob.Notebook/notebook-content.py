# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder.appName("DummySparkJob").getOrCreate()

# Dummy data
data = [
    (1, "Alice", 100),
    (2, "Bob", 200),
    (3, "Charlie", 150)
]

columns = ["id", "name", "amount"]

# Create DataFrame
df = spark.createDataFrame(data, columns)

# Simple transformation
result = df.filter(df.amount > 120)

# Show result (visible in Spark job logs)
result.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


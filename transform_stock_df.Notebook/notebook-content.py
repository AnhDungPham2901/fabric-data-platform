# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "60675e20-d05c-4f29-bfc4-ad0e9ded30a0",
# META       "default_lakehouse_name": "Lakehouse_Bronze",
# META       "default_lakehouse_workspace_id": "73ae5d61-8b64-4fb1-b84c-5fa20a6a0e8f",
# META       "known_lakehouses": [
# META         {
# META           "id": "60675e20-d05c-4f29-bfc4-ad0e9ded30a0"
# META         },
# META         {
# META           "id": "b47f0e9c-5678-452f-907b-694ece8681a0"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql import functions as F

def transform_stock(df):
    return (
        df
        .withColumn("item_price", F.substring(F.col("item_price"), 2, 1000))
        .withColumn("item_price", F.col("item_price").cast("float"))
        .groupby("item_status")
        .agg(
            F.countDistinct("item_name").alias("number_of_item"),
            F.sum("item_price").alias("total_sales"),
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

transformed_df = spark.read.format("delta").load(
    "abfss://dev@onelake.dfs.fabric.microsoft.com/Lakehouse_Bronze.Lakehouse/Tables/dbo/demo_items"
)
stock_df = transform_stock(df=transformed_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

stock_df.write.format("delta").mode("overwrite").save(
    "abfss://dev@onelake.dfs.fabric.microsoft.com/Lakehouse_Silver.Lakehouse/Tables/dbo/stock_df"
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

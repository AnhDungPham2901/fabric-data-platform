# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "b47f0e9c-5678-452f-907b-694ece8681a0",
# META       "default_lakehouse_name": "Lakehouse_Silver",
# META       "default_lakehouse_workspace_id": "73ae5d61-8b64-4fb1-b84c-5fa20a6a0e8f",
# META       "known_lakehouses": [
# META         {
# META           "id": "b47f0e9c-5678-452f-907b-694ece8681a0"
# META         },
# META         {
# META           "id": "60675e20-d05c-4f29-bfc4-ad0e9ded30a0"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

%run ./transform_stock_df

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

!pip install --quiet ipytest

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Cell 1 — setup
import ipytest
ipytest.autoconfig()

import pytest
from pyspark.sql import functions as F

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Cell 2 — helper
def _df(spark, rows, schema: str):
    return spark.createDataFrame(rows, schema)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


def test_strip_currency_and_cast():
    df = _df(
        spark,
        [("A", "$10.5", "active"), ("B", "$5.0", "active")],
        "item_name STRING, item_price STRING, item_status STRING"
    )

    result = transform_stock(df)

    values = (
        result
        .filter("item_status = 'active'")
        .select("total_sales")
        .collect()[0][0]
    )

    assert values == pytest.approx(15.5)


def test_grouping_and_count_distinct():
    df = _df(
        spark,
        [
            ("A", "$10", "active"),
            ("A", "$20", "active"),
            ("B", "$5", "inactive"),
        ],
        "item_name STRING, item_price STRING, item_status STRING"
    )

    result = transform_stock(df)

    active = result.filter("item_status = 'active'").collect()[0]
    assert active["number_of_item"] == 1


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def test_staging_table_exists():
    df = spark.read.table("Lakehouse_Bronze.dbo.demo_items")
    assert df.count() > 0


def test_staging_output_written():
    df = spark.read.table("Lakehouse_Silver.dbo.stock_df")
    assert df.count() > 0


def test_no_null_totals_in_staging():
    df = spark.read.table("Lakehouse_Silver.dbo.stock_df")
    assert df.filter("total_sales IS NULL").count() == 0


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def test_sales_reconciliation_staging():
    src = spark.read.table("Lakehouse_Bronze.dbo.demo_items")
    tgt = spark.read.table("Lakehouse_Silver.dbo.stock_df")

    src_sum = (
        src
        .withColumn("item_price", F.substring("item_price", 2, 1000).cast("float"))
        .agg(F.sum("item_price"))
        .collect()[0][0]
    )

    tgt_sum = tgt.agg(F.sum("total_sales")).collect()[0][0]

    assert abs(src_sum - tgt_sum) < 0.01

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

ipytest.run("-v")

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

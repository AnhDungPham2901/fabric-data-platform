# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "9f04346f-f2a5-478b-b201-62d9115dddae",
# META       "default_lakehouse_name": "BookHouse",
# META       "default_lakehouse_workspace_id": "73ae5d61-8b64-4fb1-b84c-5fa20a6a0e8f",
# META       "known_lakehouses": [
# META         {
# META           "id": "9f04346f-f2a5-478b-b201-62d9115dddae"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

df = spark.read.table('publicholidays')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df)

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

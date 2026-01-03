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
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
%pip install requests beautifulsoup4 pandas

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://anhdungpham2901.github.io/scrapping-demo-website/"

resp = requests.get(BASE_URL)
resp.raise_for_status()

soup = BeautifulSoup(resp.text, "html.parser")

detail_links = [
    urljoin(BASE_URL, a["href"])
    for a in soup.select("a[href^='detail_']")
]

detail_links

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

items = []

for url in detail_links:
    r = requests.get(url)
    r.raise_for_status()
    s = BeautifulSoup(r.text, "html.parser")

    item = {
        "item_name": s.select_one("h1.title").get_text(strip=True),
        "item_url": url,
        "item_price": s.select_one("li[data-key='price']").get_text(strip=True),
        "item_category": s.select_one("li[data-key='category']").get_text(strip=True),
        "item_status": s.select_one("li[data-key='stock']").get_text(strip=True),
    }

    items.append(item)

items


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import pandas as pd

df = pd.DataFrame(items)
df

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_spark = spark.createDataFrame(df)

# save to Lakehouse_Bronze.dbo
df_spark.write.mode("overwrite").saveAsTable(
    "Lakehouse_Bronze.dbo.demo_items"
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

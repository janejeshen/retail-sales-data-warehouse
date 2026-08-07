"""
Loads transformed sales into SQL Server.
"""

from database import engine
from transform_sales import sales_generator

for i, sales in enumerate(sales_generator(), start=1):

    print(f"Loading chunk {i}")

    sales.to_sql(
        "stg_sales",
        engine,
        schema="staging",
        if_exists="append",
        index=False,
        chunksize=250
    )

print("Sales loaded.")
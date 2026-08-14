"""
Sales transformation module.
Responsibilities:
    1. Read sales data in chunks.
    2. Unpivot the wide sales format.
    3. Clean text columns.
    4. Convert units sold to integers.
    5. Remove zero-sales records.
    6. Remove duplicate records within each chunk.

This does NOT load data into SQL Server.
"""

import pandas as pd
from config import SALES_CSV, CHUNK_SIZE


def transform_sales():

    """
    Generates transformed sales DataFrames one chunk at a time.
    """

    reader = pd.read_csv(
        SALES_CSV,
        chunksize=CHUNK_SIZE
    )

    for chunk in reader:

        # UNPIVOT WIDE DATA INTO LONG FORMAT

        melted = chunk.melt(
            id_vars=[
                "id",
                "item_id",
                "dept_id",
                "cat_id",
                "store_id",
                "state_id"
            ],
            var_name="d",
            value_name="units_sold"
        )

        # CLEAN TEXT COLUMNS

        for column in [
            "item_id",
            "dept_id",
            "cat_id",
            "store_id",
            "state_id"
        ]:

            melted[column] = (
                melted[column]
                .str.upper()
                .str.strip()
            )

        # CLEAN SALES VALUES

        melted["units_sold"] = (
            melted["units_sold"]
            .fillna(0)
            .astype("int32")
        )


        # REMOVE ZERO SALES

        melted = melted[
            melted["units_sold"] > 0
        ]

        # REMOVE DUPLICATES
        melted = melted.drop_duplicates()
        
        yield melted
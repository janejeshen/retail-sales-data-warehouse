"""
Reads the raw sales file in chunks, unpivots it,
performs basic cleaning and yields transformed chunks.
"""

import pandas as pd

from config import SALES_CSV, CHUNK_SIZE


def sales_generator():
    """
    Yield transformed chunks of sales data.

    Each yielded DataFrame has columns:
        id, item_id, dept_id, cat_id,
        store_id, state_id, d, units_sold
    """

    reader = pd.read_csv(
        SALES_CSV,
        chunksize=CHUNK_SIZE
    )

    for chunk in reader:

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

        # Basic cleaning
        for col in [
            "item_id",
            "dept_id",
            "cat_id",
            "store_id",
            "state_id"
        ]:
            melted[col] = melted[col].str.upper().str.strip()

        melted["units_sold"] = (
            melted["units_sold"]
            .fillna(0)
            .astype(int)
        )

        melted = melted[melted["units_sold"] > 0]

        melted = melted.drop_duplicates()

        yield melted
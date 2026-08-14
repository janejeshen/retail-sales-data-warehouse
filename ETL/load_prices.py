"""
Load Walmart sell-price data into SQL Server staging.
Features:
    - Prevents duplicate batches using etl_load_history.
    - Loads the CSV in chunks.
    - Uses a fresh SQLAlchemy connection for each chunk.
    - Properly handles transaction failures.
"""

import os
import time
import pandas as pd
from config import (
    PRICES_CSV,
    PRICES_DATASET,
    SQL_BATCH_SIZE
)

from database import engine
from database_utils import (
    batch_already_loaded,
    start_batch,
    complete_batch,
    fail_batch
)


# LOAD PRICES

def load_prices(
    source_file: str = PRICES_CSV,
    batch_id: str = "M5_PRICES_001"
):

    print("\n" + "=" * 60)
    print("WALMART PRICE ETL")
    print("=" * 60)

    print(f"Source : {source_file}")
    print(f"Batch  : {batch_id}")


    # CHECK WHETHER THE BATCH ALREADY EXISTS

    if batch_already_loaded(
        PRICES_DATASET,
        batch_id
    ):

        print(
            f"\nPrice batch '{batch_id}' "
            "has already been loaded."
        )

        print("Skipping price load.")

        return

    # CHECK FILE
    if not os.path.exists(source_file):

        raise FileNotFoundError(
            f"Price file not found:\n{source_file}"
        )

    # REGISTER BATCH
    start_batch(
        dataset_name=PRICES_DATASET,
        source_file=source_file,
        batch_id=batch_id
    )


    start_time = time.time()

    total_inserted = 0


    try:
        # READ CSV IN CHUNKS
        reader = pd.read_csv(
            source_file,
            chunksize=100_000
        )


        for chunk_number, chunk in enumerate(
            reader,
            start=1
        ):

            print(
                f"\nProcessing Price Chunk "
                f"{chunk_number}"
            )

            # BASIC CLEANING
            text_columns = [
                "store_id",
                "item_id"
            ]


            for column in text_columns:

                if column in chunk.columns:

                    chunk[column] = (
                        chunk[column]
                        .astype(str)
                        .str.upper()
                        .str.strip()
                    )


            # CLEAN NUMERIC COLUMNS

            if "wm_yr_wk" in chunk.columns:

                chunk["wm_yr_wk"] = pd.to_numeric(
                    chunk["wm_yr_wk"],
                    errors="coerce"
                ).astype("Int64")


            if "sell_price" in chunk.columns:

                chunk["sell_price"] = pd.to_numeric(
                    chunk["sell_price"],
                    errors="coerce"
                )

            # REMOVE INVALID RECORDS
            chunk = chunk.dropna(
                subset=[
                    "store_id",
                    "item_id",
                    "wm_yr_wk"
                ]
            )

            # REMOVE DUPLICATES WITHIN CHUNK
            chunk = chunk.drop_duplicates()


            if len(chunk) == 0:

                print(
                    "No valid rows in this chunk."
                )

                continue


            # INSERT USING A FRESH CONNECTION

            with engine.begin() as connection:

                chunk.to_sql(
                    name="stg_sell_prices",
                    schema="staging",
                    con=connection,
                    if_exists="append",
                    index=False,
                    chunksize=SQL_BATCH_SIZE
                )


            rows_inserted = len(chunk)

            total_inserted += rows_inserted


            print(
                f"Inserted {rows_inserted:,} rows"
            )

        # MARK SUCCESS
        complete_batch(
            dataset_name=PRICES_DATASET,
            batch_id=batch_id,
            rows_loaded=total_inserted
        )


        elapsed = time.time() - start_time


        print("\n" + "=" * 60)
        print("PRICE IMPORT COMPLETED")
        print("=" * 60)

        print(
            f"Rows Inserted : {total_inserted:,}"
        )

        print(
            f"Time Taken    : "
            f"{elapsed / 60:.2f} minutes"
        )


    except Exception as error:

        # RECORD FAILURE

        fail_batch(
            dataset_name=PRICES_DATASET,
            batch_id=batch_id,
            error_message=str(error)
        )


        print("\n" + "=" * 60)
        print("PRICE IMPORT FAILED")
        print("=" * 60)

        print(
            f"Error: {error}"
        )


        raise

# RUN DIRECTLY
if __name__ == "__main__":

    load_prices()
"""
Sales loader.

Supports multiple batches without loading the same batch twice.
"""

import os
import time

from config import (
    SALES_DATASET,
    SALES_CSV,
    SQL_BATCH_SIZE
)

from database import engine

from database_utils import (
    batch_already_loaded,
    start_batch,
    complete_batch,
    fail_batch
)

from transform_sales import transform_sales


def load_sales(
    source_file: str = SALES_CSV,
    batch_id: str = "M5_VALIDATION_001"
):
    """
    Load a sales batch into staging.
    The batch_id uniquely identifies the source batch.
    If the batch has already successfully loaded, the function
    exits without inserting anything.
    """

    # CHECKING WHETHER BATCH WAS ALREADY LOADED

    if batch_already_loaded(
        SALES_DATASET,
        batch_id
    ):
        print("=" * 60)

        print(f"Batch '{batch_id}' has already been loaded.")

        print("Skipping sales load.")

        print("=" * 60)

        return

    # VALIDATING SOURCE FILE

    if not os.path.exists(source_file):

        raise FileNotFoundError(f"Sales source file not found: {source_file}")

    # REGISTERING BATCH

    start_batch(
        dataset_name=SALES_DATASET,
        source_file=source_file,
        batch_id=batch_id)


    print("=" * 60)
    print("WALMART SALES ETL")
    print("=" * 60)

    print(f"Source : {source_file}")
    print(f"Batch  : {batch_id}")


    start_time = time.time()

    total_inserted = 0


    try:
        # PROCESSING CHUNKS
        for chunk_number, melted in enumerate(
            transform_sales(),
            start=1
        ):

            print(f"\nProcessing Chunk {chunk_number}")

            # LOADING CHUNK

            melted.to_sql(
                name="stg_sales",
                schema="staging",
                con=engine,
                if_exists="append",
                index=False,
                chunksize=SQL_BATCH_SIZE)


            rows = len(melted)

            total_inserted += rows


            print(f"Inserted {rows:,} rows")

        # MARKING BATCH AS SUCCESSFUL

        complete_batch(
            dataset_name=SALES_DATASET,
            batch_id=batch_id,
            rows_loaded=total_inserted
        )

        elapsed = time.time() - start_time

        print("\n" + "=" * 60)
        print("IMPORT COMPLETED")
        print("=" * 60)

        print(f"Batch ID: {batch_id}")

        print(f"Rows Inserted: {total_inserted:,}")

        print(f"Time Taken: {elapsed / 60:.2f} minutes")

    except Exception as error:
        # RECORDING FAILURE
        fail_batch(
            dataset_name=SALES_DATASET,
            batch_id=batch_id,
            error_message=str(error))

        print(f"Sales batch failed: {error}")

        raise


if __name__ == "__main__":

    load_sales(source_file=SALES_CSV,batch_id="M5_VALIDATION_001")
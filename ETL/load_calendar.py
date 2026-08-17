"""
Calendar data loader.
Uses batch tracking to prevent duplicate loads.
"""

import os
import pandas as pd
from config import (CALENDAR_CSV,CALENDAR_DATASET)

from database import engine
from database_utils import (
    batch_already_loaded,
    start_batch,
    complete_batch,
    fail_batch)


def load_calendar(
    source_file: str = CALENDAR_CSV,
    batch_id: str = "M5_CALENDAR_001"
):

    # Check whether this batch was already loaded.

    if batch_already_loaded(
        CALENDAR_DATASET,
        batch_id ):

        print(f"Calendar batch '{batch_id}' already loaded. "
            "Skipping.")

        return


    if not os.path.exists(source_file):

        raise FileNotFoundError("Calendar file not found: {source_file}")


    start_batch(
        dataset_name=CALENDAR_DATASET,
        source_file=source_file,
        batch_id=batch_id
    )


    try:

        calendar = pd.read_csv(source_file)


        calendar.to_sql(
            name="stg_calendar",
            schema="staging",
            con=engine,
            if_exists="append",
            index=False
        )


        complete_batch(
            dataset_name=CALENDAR_DATASET,
            batch_id=batch_id,
            rows_loaded=len(calendar)
        )


        print(
            f"Calendar loaded: {len(calendar):,} rows"
        )


    except Exception as error:

        fail_batch(dataset_name=CALENDAR_DATASET,batch_id=batch_id,error_message=str(error))

        raise


if __name__ == "__main__":

    load_calendar()
"""
Reusable database functions for the Walmart BI ETL pipeline.

This module handles:

1. Checking whether a batch has already succeeded.
2. Starting a new batch.
3. Restarting a failed/interrupted batch.
4. Marking a batch as successful.
5. Marking a batch as failed.
"""

from datetime import datetime

from sqlalchemy import text

from database import engine


# ================================================================
# CHECK WHETHER A BATCH WAS SUCCESSFULLY LOADED
# ================================================================

def batch_already_loaded(
    dataset_name: str,
    batch_id: str
) -> bool:
    """
    Check whether a dataset + batch combination has already
    completed successfully.

    Returns:
        True  -> batch already succeeded
        False -> batch has not succeeded
    """

    query = text(
        """
        SELECT COUNT(*)
        FROM staging.etl_load_history

        WHERE dataset_name = :dataset_name
          AND batch_id = :batch_id
          AND status = 'SUCCESS'
        """
    )

    with engine.connect() as connection:

        count = connection.execute(
            query,
            {
                "dataset_name": dataset_name,
                "batch_id": batch_id
            }
        ).scalar()

    return count > 0


# ================================================================
# CHECK WHETHER A BATCH EXISTS
# ================================================================

def batch_exists(
    dataset_name: str,
    batch_id: str
) -> bool:
    """
    Check whether any history record exists for the batch.

    This includes:

        RUNNING
        SUCCESS
        FAILED
    """

    query = text(
        """
        SELECT COUNT(*)
        FROM staging.etl_load_history

        WHERE dataset_name = :dataset_name
          AND batch_id = :batch_id
        """
    )

    with engine.connect() as connection:

        count = connection.execute(
            query,
            {
                "dataset_name": dataset_name,
                "batch_id": batch_id
            }
        ).scalar()

    return count > 0


# ================================================================
# START OR RESTART A BATCH
# ================================================================

def start_batch(
    dataset_name: str,
    source_file: str,
    batch_id: str
):
    """
    Start a new batch.

    If the batch does not exist:
        Create a new history record.

    If the batch exists with FAILED/RUNNING:
        Reset it to RUNNING.

    If the batch already SUCCESS:
        Do nothing.

    The UNIQUE constraint on
        dataset_name + batch_id
    is therefore respected.
    """

    # ------------------------------------------------------------
    # Check existing batch
    # ------------------------------------------------------------

    query = text(
        """
        SELECT
            status

        FROM staging.etl_load_history

        WHERE dataset_name = :dataset_name
          AND batch_id = :batch_id
        """
    )

    with engine.connect() as connection:

        result = connection.execute(
            query,
            {
                "dataset_name": dataset_name,
                "batch_id": batch_id
            }
        ).fetchone()


    # ============================================================
    # CASE 1 — BATCH DOES NOT EXIST
    # ============================================================

    if result is None:

        insert_query = text(
            """
            INSERT INTO staging.etl_load_history
            (
                dataset_name,
                source_file,
                batch_id,
                rows_loaded,
                load_started,
                load_completed,
                status,
                error_message
            )

            VALUES
            (
                :dataset_name,
                :source_file,
                :batch_id,
                NULL,
                :load_started,
                NULL,
                'RUNNING',
                NULL
            )
            """
        )

        with engine.begin() as connection:

            connection.execute(
                insert_query,
                {
                    "dataset_name": dataset_name,
                    "source_file": source_file,
                    "batch_id": batch_id,
                    "load_started": datetime.now()
                }
            )

        return


    # ============================================================
    # EXISTING STATUS
    # ============================================================

    existing_status = result.status


    # ============================================================
    # CASE 2 — ALREADY SUCCESSFUL
    # ============================================================

    if existing_status == "SUCCESS":

        print(
            f"Batch '{batch_id}' already completed successfully."
        )

        return


    # ============================================================
    # CASE 3 — FAILED OR INTERRUPTED
    # ============================================================

    update_query = text(
        """
        UPDATE staging.etl_load_history

        SET
            source_file = :source_file,
            rows_loaded = NULL,
            load_started = :load_started,
            load_completed = NULL,
            status = 'RUNNING',
            error_message = NULL

        WHERE dataset_name = :dataset_name
          AND batch_id = :batch_id
        """
    )

    with engine.begin() as connection:

        connection.execute(
            update_query,
            {
                "dataset_name": dataset_name,
                "batch_id": batch_id,
                "source_file": source_file,
                "load_started": datetime.now()
            }
        )

    print(
        f"Restarting existing batch '{batch_id}'."
    )


# ================================================================
# COMPLETE BATCH
# ================================================================

def complete_batch(
    dataset_name: str,
    batch_id: str,
    rows_loaded: int
):
    """
    Mark a batch as successfully completed.
    """

    query = text(
        """
        UPDATE staging.etl_load_history

        SET
            rows_loaded = :rows_loaded,
            load_completed = :load_completed,
            status = 'SUCCESS',
            error_message = NULL

        WHERE dataset_name = :dataset_name
          AND batch_id = :batch_id
        """
    )

    with engine.begin() as connection:

        connection.execute(
            query,
            {
                "dataset_name": dataset_name,
                "batch_id": batch_id,
                "rows_loaded": rows_loaded,
                "load_completed": datetime.now()
            }
        )


# ================================================================
# FAIL BATCH
# ================================================================

def fail_batch(
    dataset_name: str,
    batch_id: str,
    error_message: str
):
    """
    Mark a batch as failed.

    The history record remains in the database so that the
    next execution can restart it instead of creating a
    duplicate history record.
    """

    query = text(
        """
        UPDATE staging.etl_load_history

        SET
            status = 'FAILED',
            error_message = :error_message,
            load_completed = :load_completed

        WHERE dataset_name = :dataset_name
          AND batch_id = :batch_id
        """
    )

    with engine.begin() as connection:

        connection.execute(
            query,
            {
                "dataset_name": dataset_name,
                "batch_id": batch_id,
                "error_message": error_message,
                "load_completed": datetime.now()
            }
        )
"""
Creates the ETL load history table.
The table prevents the same batch from being loaded multiple times.
"""

from database import engine

CREATE_ETL_HISTORY_TABLE = """

IF OBJECT_ID('staging.etl_load_history', 'U') IS NULL

BEGIN

    CREATE TABLE staging.etl_load_history
    (
        load_id INT IDENTITY(1,1) PRIMARY KEY
        dataset_name VARCHAR(100) NOT NULL,
        source_file VARCHAR(500) NOT NULL,
        batch_id VARCHAR(100) NOT NULL,
        rows_loaded BIGINT NULL,
        load_started DATETIME2 NULL,
        load_completed DATETIME2 NULL,
        status VARCHAR(20) NOT NULL,
        error_message VARCHAR(MAX) NULL,
        created_at DATETIME2 NOT NULL
            DEFAULT SYSDATETIME(),
        CONSTRAINT UQ_ETL_DATASET_BATCH
            UNIQUE(dataset_name, batch_id)
    );

END;

"""

def create_etl_history_table():

    with engine.begin() as connection:

        connection.exec_driver_sql(
            CREATE_ETL_HISTORY_TABLE
        )

    print(
        "ETL load history table checked successfully."
    )


if __name__ == "__main__":
    create_etl_history_table()
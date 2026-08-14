"""
SQL Server database connection.
All ETL modules import the SQLAlchemy engine from this file.
"""

import urllib
from sqlalchemy import create_engine
from config import SERVER, DATABASE

# SQL SERVER CONNECTION

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
)

engine = create_engine(
    (
        "mssql+pyodbc:///?odbc_connect="
        f"{urllib.parse.quote_plus(connection_string)}"
    ),
    fast_executemany=True
)
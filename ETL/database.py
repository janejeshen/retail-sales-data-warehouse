"""
Creating a reusable SQL Server engine.
Every file simply imports:
from database import engine
"""

import urllib
from sqlalchemy import create_engine
from config import SERVER, DATABASE

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
)

engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}",
    fast_executemany=True
)
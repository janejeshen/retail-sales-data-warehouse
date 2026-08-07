"""
Creates WalmartBI database if it does not exist.
"""

import pyodbc
from config import SERVER

connection = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    "DATABASE=master;"
    "Trusted_Connection=yes;"
)

cursor = connection.cursor()

cursor.execute("""

IF DB_ID('WalmartBI') IS NULL

BEGIN

CREATE DATABASE WalmartBI

END

""")

connection.commit()

print("Database checked.")
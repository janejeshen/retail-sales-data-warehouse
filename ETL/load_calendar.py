"""
Loads calendar.csv into staging.stg_calendar.
"""

import pandas as pd

from database import engine
from config import CALENDAR_CSV

calendar = pd.read_csv(CALENDAR_CSV)

calendar.to_sql(
    "stg_calendar",
    engine,
    schema="staging",
    if_exists="append",
    index=False
)

engine.dispose()

print("Calendar loaded.")
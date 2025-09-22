import pandas as pd 
import sqlite3
import numpy as np 
import os

f1_info = pd.read_csv("data/f1_merged_database.csv")

conn = sqlite3.connect("f1_final_database.db")

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS f1_merged (
        raceId INT,
        date DATE,
        year INT,
        name TEXT,
        driverId INT,
        constructorId INT,
        grid INT,
        position INT,
        forename TEXT,
        surname TEXT,
        constructor_name TEXT,
        constructor_points INT,
        podium INT
    );    """)

conn.commit()

drivers = f1_info[["forename," "surname"]].drop_duplicates()
drivers.columns = ["driver_names"]

constructors = f1_info[["constructor_name"]].drop_duplicates()
constructors.columns = ["constructor_names"]

tracks = f1_info[["name"]].drop_duplicates()
tracks.columns = ["GP_track_names"]

f1_info.to_sql("f1_merged", conn, if_exists = "append", index = False)
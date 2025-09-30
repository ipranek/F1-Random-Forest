import pandas as pd 
import sqlite3
import numpy as np 
import os

f1_info = pd.read_csv("/Users/ipekoner/Documents/GitHub/F1-Random-Forest/data/f1_merged_database.csv")

conn = sqlite3.connect("f1_final_database.db")

cursor = conn.cursor()

print("Dropping existing tables...")
cursor.execute("DROP TABLE IF EXISTS f1_merged")
cursor.execute("DROP TABLE IF EXISTS drivers")
cursor.execute("DROP TABLE IF EXISTS constructors")
cursor.execute("DROP TABLE IF EXISTS tracks")

print("creating new tables")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS f1_merged (
        raceId INT,
        date DATE,
        year INT,
        name TEXT,
        driverId INT,
        driver_fullname TEXT,
        constructorId INT,
        grid INT,
        position INT,
        forename TEXT,
        surname TEXT,
        constructor_name TEXT,
        constructor_points INT,
        podium INT,
        driverId_encoded INT,
        constructorId_encoded INT,
        GP_name_encoded INT
               
    );    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS drivers(
               driverId_encoded INT PRIMARY KEY,
               driver_fullname TEXT UNIQUE); """)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS constructors(
               constructorId_encoded INT PRIMARY KEY,
               constructor_name TEXT UNIQUE); """)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tracks(
               GP_name_encoded INT PRIMARY KEY,
               GP_track_name TEXT UNIQUE); """)

print("committing changes")
conn.commit()
print("is the porblem here")

drivers = f1_info[["driver_fullname"]].drop_duplicates().reset_index(drop=True)
#drivers["driver_names"] = drivers["forename"] + " " + drivers["surname"]

drivers["driverId_encoded"] = drivers.index
print("inserting")
drivers.to_sql("drivers", conn, if_exists ="append", index=False)


constructors = f1_info[["constructor_name"]].drop_duplicates().reset_index(drop=True)
constructors["constructorId_encoded"] = constructors.index
print("inserting")
constructors.to_sql("constructors", conn, if_exists ="append", index=False)

tracks = f1_info[["name"]].drop_duplicates().reset_index(drop=True)
tracks = tracks.rename(columns={"name": "GP_track_name"})
tracks["GP_name_encoded"] = tracks.index
print("inserting")
tracks.to_sql("tracks", conn, if_exists="replace", index=False)
print("inserting")
f1_info.to_sql("f1_merged", conn, if_exists = "append", index = False)
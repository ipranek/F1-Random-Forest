from flask import Flask, render_template, jsonify
import sqlite3
import pandas as pd
import numpy as np
from flask_cors import CORS


app = Flask(__name__)

DB_PATH = "/Users/ipekoner/Documents/GitHub/F1-Random-Forest/database/f1_final_database.db"

#model = 

@app.route("/", methods = ["GET"])
def home():
    drivers = get_drivers()
    constructors = get_constructor()
    tracks = get_track()
    return render_template("home.html", drivers = drivers, constructors = constructors, tracks=tracks)
def get_drivers():
    connection_db = sqlite3.connect(DB_PATH)
    query = "SELECT driverId_encoded, driver_fullname FROM drivers" #later go and change the sql table and include the driver_fullname, no need for the concetenation in the sql
    drivers = pd.read_sql(query, connection_db)
    connection_db.close()
    return drivers.to_dict(orient = "records")
def get_constructor():
    connection_db = sqlite3.connect(DB_PATH)
    query = "SELECT constructorId_encoded, constructor_names FROM constructors" #lowkey check var name, names or name
    constructors = pd.read_sql(query, connection_db)
    connection_db.close
    return constructors.to_dict(orient = "records")
def get_track():
    connection_db = sqlite3.connect(DB_PATH)
    query = "SELECT GP_name_encoded, GP_track_name FROM tracks"
    tracks = pd.read_sql(query, connection_db)
    connection_db.close()
    return tracks.to_dict(orient = "records")
if __name__ == "__main__":
    app.run(debug=True, port=5001)




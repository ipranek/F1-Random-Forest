from flask import Flask, render_template, jsonify
import sqlite3
import pandas as pd
import numpy as np
from flask_cors import CORS


app = Flask(__name__)

#DB_PATH =

#model = 

@app.route("/", methods = ["GET"])
def home():
    drivers = get_drivers()
    constructors = get_constructors()
    tracks = get_tracks()
    return render_template("home.html", drivers = drivers, constructors = constructors, tracks=tracks)
def get_drivers():
    connection_db = sqlite3.connect(DB_PATH)
    query = "SELECT driverId_encoded from drivers WHERE driver_names" #later go and change the sql table and include the driver_fullname, no need for the concetenation in the sql
    drivers = pd.read_sql(query, connection_db)
    connection_db.close()
    return drivers.to_dict(orient = "records")
def get_constructor():
    connection_db = sqlite3.connect(DB_PATH)
    query = "SELECT constructorId_encoded from constructors WHERE constructor_names" #lowkey check var name, names or name
    constructors = pd.read_Sql(query, connection_db)
    connection_db.close
if __name__ == "main":
    app.run(debug=True, port=5001)




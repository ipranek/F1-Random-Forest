from flask import Flask, render_template, jsonify, request
import sqlite3
import pandas as pd
import numpy as np
from flask_cors import CORS



app = Flask(__name__)

DB_PATH = "/Users/ipekoner/Documents/GitHub/F1-Random-Forest/database/f1_final_database.db"

rf_class_model = "/Users/ipekoner/Documents/GitHub/F1-Random-Forest/rf_podium_model.joblib"
rf_reg_model = "/Users/ipekoner/Documents/GitHub/F1-Random-Forest/rf_position_model.joblib"

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
def predict():
    merged = request.json
    driver_name = merged["driver_fullname"]
    constructor_name = merged["constructor_name"]
    track_name = merged["GP_track_name"]
    grid_position = merged.get("grid", 1)

    conn = sqlite3.connect(DB_PATH)

    driver_id_encoded = pd.read_sql( "SELECT driverId_encoded FROM drivers WHERE driver_fullname = ?", conn, params=(driver_name,)).iloc[0,0]
    constructor_id_encoded = pd.read_sql("SELECT constructorId_encoded FROM constructors WHERE constructor_name", conn, params=(constructor_name,)).iloc[0,0]
    track_id_encoded = pd.read_sql( "SELECT GP_name_encoded FROM tracks WHERE GP_track_name = ?", conn, params=(track_name,)).iloc[0,0]

    stats = pd.read_sql(
        """
        SELECT constructor_points_avg, constructor_points_sum, season_avg_position, season_avg_delta FROM f1_merged
        WHERE driverId_encoded = ? AND constructorId_encoded = ? AND GP_name_encoded = ?
        ORDER BY date DESC LIMIT 1
        """, conn, params = (driver_id_encoded, constructor_id_encoded, track_id_encoded))
    conn.close()

    stats_dict = stats.iloc[0].to_dict() #takes the dataframe stats and gets the first row of said dataframe, returns as pandas series, turns into dict

    input_df = pd.DataFrame([{
        "driverId_encoded": driver_id_encoded,
        "constructorId_encoded": constructor_id_encoded,
        "GP_name_encoded": track_id_encoded,
        "constructor_points_avg": stats_dict["constructor_points_avg"],
        "constructor_points_sum": stats_dict["constructor_points_sum"],
        "season_avg_position": stats_dict["season_avg_position"],
        "season_avg_delta": stats_dict["seaosn_avg_delta"],
        "grid": grid_position

    }])

    predicted_position =rf_reg_model.predict(input_df)[0] #predict gives array, [0] to extract first and singular scalar value from the array
    podium = predicted_position <= 3
    return jsonify({ #cannot handle numpy arrays directly
        "predicted_potision": float(predicted_position),
        "podium": podium
    })
    
if __name__ == "__main__":
    app.run(debug=True, port=5001)




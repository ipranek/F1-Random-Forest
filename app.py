from flask import Flask, render_template, jsonify
import sqlite3
import pandas as pd
import numpy as np
from flask_cors import CORS


app = Flask(__name__)

#DB_PATH =

#model = 

@app.route("/")
def home():
    return render_template("home.html")
if __name__ == "main":
    app.run(debug=True, port=5001)




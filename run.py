import serial
from flask import Flask
from migrations.setup import SetupMigration
from flask import jsonify, send_file
import sqlite3
from data_reader import DataReader

# Initialize the flask app
app = Flask(__name__)
ser = serial.Serial('/dev/ttyS1', 19200, timeout=1)

@app.route("/")
def default():
    return send_file("./chartdisplay.html")

@app.route("/api/getMeasurementData")
def getMeasurementData():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    results = cur.execute("SELECT * FROM `measurement_data`").fetchall()
    data = []
    for el in results:
        data.append({
            "ID": el[0],
            "timestamp": el[1],
            "dimmFactor": el[2],
            "voltage": el[3],
            "angle": el[4]
        })
    return jsonify({
        "results": data
    })

@app.route("/api/updateValues/<dimm>/<angle>")
def updateAngle(dimm, angle):
    dimmValue = int(dimm)
    angleValue = int(angle)
    ser.write(f"{dimmValue};{angleValue}\n")
    return ""




if __name__ == '__main__':
    conn = sqlite3.connect("database.db")
    SetupMigration(conn)
    conn.close()
    ser.open()
    reader = DataReader(serial=ser)
    reader.start()
    app.run(host="0.0.0.0", port=8080)
    reader.join()

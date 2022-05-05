import threading
import time
import sqlite3


class DataReader(threading.Thread):
    def __init__(self, serial):
        threading.Thread.__init__(self)
        self.serial = serial

    def run(self) -> None:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        while True:
            line = str(self.serial.readline())
            parts = line.split(";")
            #parts = [1, 2, 3]
            cur.execute("""
            INSERT INTO measurement_data (ID, timestamp, dimmFactor, voltage, angle)
VALUES (null, ?, ?, ?, ?);
            """, [int(time.time()), parts[0], parts[1], parts[2]])
            conn.commit()
            time.sleep(1)

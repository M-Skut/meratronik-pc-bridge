import time
import random
import sqlite3 as sqlite
import os

if not os.path.isfile('meratronik_data.db'):
    print("Database does not exist, creating new one...")
    conn = sqlite.connect('meratronik_data.db')
    with conn:
        conn = conn.cursor()
        conn.execute(
            "CREATE TABLE meratronik_data(timestamp DATETIME, voltage NUMERIC, current NUMERIC)")


while True:
    try:
        conn = sqlite.connect('meratronik_data.db')
    except IOError as e:
        exit(1)
    with conn:
        voltage, current = (random.randint(1, 10)*0.1, random.randint(1, 10)*0.01)
        conn = conn.cursor()
        conn.execute(
            "INSERT INTO meratronik_data VALUES(datetime('now', 'localtime'), (?), (?))", (voltage, current))
    # Flush data and wait
    time.sleep(5)

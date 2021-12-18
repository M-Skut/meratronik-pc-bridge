import json
import random
import time
from datetime import datetime
import sqlite3 as sqlite

from flask import Flask, Response, render_template, g, make_response

DB_PATH = 'web-application/meratronik_data.db'

sql_queries = {
    ('current', 'all'): "SELECT timestamp, current FROM meratronik_data ORDER BY timestamp DESC LIMIT 2000",
    ('voltage', 'all'): "SELECT timestamp, voltage FROM meratronik_data ORDER BY timestamp DESC LIMIT 2000",
}

application = Flask(__name__)


@application.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite.connect(DB_PATH)
    return db


@application.route('/')
def index():
    return render_template('index.html')


def generate_livechart(meas_type, samples_age):
    cur = get_db().cursor()
    cur.execute(sql_queries[(meas_type, samples_age)])
    data = cur.fetchall()
    timestamps, voltage, current = [], [], []
    if meas_type == 'voltage':
        for row in reversed(data):
            timestamps.append(str(row[0]))
            voltage.append(row[1])

        result = make_response(render_template(
            'livechart_voltage.js', timestamps=timestamps, volt_data=voltage))
    elif meas_type == 'current':
        for row in reversed(data):
            timestamps.append(str(row[0]))
            current.append(row[1])

        result = make_response(render_template(
            'livechart_current.js', timestamps=timestamps, amp_data=current))

    result.headers.set('Content-type', 'text/javascript')
    return result


@application.route('/livechart_voltage.js')
def livechart_voltage():
    return generate_livechart(meas_type='voltage', samples_age='all')


@application.route('/livechart_current.js')
def livechart_current():
    return generate_livechart(meas_type='current', samples_age='all')


if __name__ == '__main__':
    application.run(debug=True, threaded=True)

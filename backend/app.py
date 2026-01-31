import json
from flask import Flask, render_template, jsonify
import os
from datetime import datetime, timedelta

app = Flask(__name__, 
    template_folder='../frontend/src/templates',
    static_folder='../static'
)

# JSON数据文件路径
DATA_FILE = '../data/aviation_data.json'

def load_data():
    """加载JSON数据"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {"flights": [], "airports": []}

def save_data(data):
    """保存JSON数据"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/flight-trends')
def get_flight_trends():
    data = load_data()
    # 直接返回JSON中的flight_trends数据
    flight_trends = data.get('flight_trends', [])
    return jsonify(flight_trends)

@app.route('/api/airport-stats')
def get_airport_stats():
    data = load_data()
    # 直接返回JSON中的airport_stats数据
    airport_stats = data.get('airport_stats', [])
    return jsonify(airport_stats)

@app.route('/api/aircraft-types')
def get_aircraft_types():
    data = load_data()
    # 直接返回JSON中的aircraft_types数据
    aircraft_types = data.get('aircraft_types', [])
    return jsonify(aircraft_types)

@app.route('/api/airlines-market-share')
def get_airlines_market_share():
    data = load_data()
    # 直接返回JSON中的airlines_market_share数据
    airlines_market_share = data.get('airlines_market_share', [])
    return jsonify(airlines_market_share)

@app.route('/api/flight-statuses')
def get_flight_statuses():
    data = load_data()
    # 直接返回JSON中的flight_statuses数据
    flight_statuses = data.get('flight_statuses', [])
    return jsonify(flight_statuses)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from datetime import datetime

app = Flask(__name__, template_folder='../frontend/src/templates')
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aviation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 数据模型定义
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photographer_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    contact_info = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FlightEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(20), nullable=False)
    airline = db.Column(db.String(100))
    aircraft_type = db.Column(db.String(50))
    departure = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    scheduled_time = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='scheduled')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AviationEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    event_type = db.Column(db.String(50))  # airshow, exhibition, etc.
    location = db.Column(db.String(200))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)
    website = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 路由定义
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appointments')
def appointments():
    appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=appointments)

@app.route('/adsb-tracker')
def adsb_tracker():
    return render_template('adsb-tracker.html')

@app.route('/calendar')
def calendar():
    events = AviationEvent.query.order_by(AviationEvent.start_date).all()
    return render_template('calendar.html', events=events)

@app.route('/special-flights')
def special_flights():
    flights = FlightEvent.query.filter(FlightEvent.status != 'completed').order_by(FlightEvent.scheduled_time).all()
    return render_template('special-flights.html', flights=flights)

@app.route('/atc-streams')
def atc_streams():
    return render_template('atc-streams.html')

# API路由
@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    appointment = Appointment(
        photographer_name=data['photographer_name'],
        location=data['location'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        description=data.get('description'),
        contact_info=data['contact_info']
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify({'status': 'success', 'id': appointment.id})

@app.route('/api/flights', methods=['POST'])
def create_flight_event():
    data = request.get_json()
    flight = FlightEvent(
        flight_number=data['flight_number'],
        airline=data.get('airline'),
        aircraft_type=data.get('aircraft_type'),
        departure=data.get('departure'),
        destination=data.get('destination'),
        scheduled_time=datetime.strptime(data['scheduled_time'], '%Y-%m-%dT%H:%M:%S'),
        status=data.get('status', 'scheduled')
    )
    db.session.add(flight)
    db.session.commit()
    return jsonify({'status': 'success', 'id': flight.id})

@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.get_json()
    event = AviationEvent(
        title=data['title'],
        event_type=data['event_type'],
        location=data.get('location'),
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None,
        description=data.get('description'),
        website=data.get('website')
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'status': 'success', 'id': event.id})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
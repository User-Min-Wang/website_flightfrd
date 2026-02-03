from extensions import db
from datetime import datetime
from sqlalchemy import Index


class Flight(db.Model):
    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(10), index=True)  # e.g., AA123
    callsign = db.Column(db.String(10), index=True)  # Radio callsign
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircraft.id'), nullable=False)
    departure_airport = db.Column(db.String(10), index=True)  # ICAO code
    arrival_airport = db.Column(db.String(10), index=True)  # ICAO code
    departure_time = db.Column(db.DateTime)  # Scheduled departure
    arrival_time = db.Column(db.DateTime)  # Scheduled arrival
    actual_departure = db.Column(db.DateTime)  # Actual departure
    actual_arrival = db.Column(db.DateTime)  # Actual arrival
    status = db.Column(db.String(20), default='scheduled')  # scheduled, active, landed, cancelled
    origin_country = db.Column(db.String(100))  # Origin country
    destination_country = db.Column(db.String(100))  # Destination country
    altitude = db.Column(db.Integer)  # Current altitude in feet
    ground_speed = db.Column(db.Float)  # Ground speed in knots
    vertical_rate = db.Column(db.Float)  # Vertical rate in ft/min
    heading = db.Column(db.Float)  # Heading in degrees
    latitude = db.Column(db.Float, index=True)  # Current latitude
    longitude = db.Column(db.Float, index=True)  # Current longitude
    on_ground = db.Column(db.Boolean, default=False)  # Whether aircraft is on ground
    squawk = db.Column(db.String(4))  # Transponder code
    baro_altitude = db.Column(db.Integer)  # Barometric altitude
    true_track = db.Column(db.Float)  # True track angle
    last_position_update = db.Column(db.DateTime)  # Last position update timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    positions = db.relationship('FlightPosition', backref='flight', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Flight {self.flight_number} - {self.callsign}>'

    def to_dict(self):
        """Convert flight object to dictionary representation"""
        return {
            'id': self.id,
            'flight_number': self.flight_number,
            'callsign': self.callsign,
            'aircraft_id': self.aircraft_id,
            'departure_airport': self.departure_airport,
            'arrival_airport': self.arrival_airport,
            'departure_time': self.departure_time.isoformat() if self.departure_time else None,
            'arrival_time': self.arrival_time.isoformat() if self.arrival_time else None,
            'actual_departure': self.actual_departure.isoformat() if self.actual_departure else None,
            'actual_arrival': self.actual_arrival.isoformat() if self.actual_arrival else None,
            'status': self.status,
            'origin_country': self.origin_country,
            'destination_country': self.destination_country,
            'altitude': self.altitude,
            'ground_speed': self.ground_speed,
            'vertical_rate': self.vertical_rate,
            'heading': self.heading,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'on_ground': self.on_ground,
            'squawk': self.squawk,
            'baro_altitude': self.baro_altitude,
            'true_track': self.true_track,
            'last_position_update': self.last_position_update.isoformat() if self.last_position_update else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class FlightPosition(db.Model):
    __tablename__ = 'flight_positions'

    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    altitude = db.Column(db.Integer)  # Altitude in feet
    ground_speed = db.Column(db.Float)  # Ground speed in knots
    heading = db.Column(db.Float)  # Heading in degrees
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)  # Position timestamp

    def __repr__(self):
        return f'<FlightPosition {self.flight_id} - {self.timestamp}>'

    def to_dict(self):
        """Convert flight position object to dictionary representation"""
        return {
            'id': self.id,
            'flight_id': self.flight_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'altitude': self.altitude,
            'ground_speed': self.ground_speed,
            'heading': self.heading,
            'timestamp': self.timestamp.isoformat()
        }


# Create composite index for efficient flight tracking
Index('idx_flight_position_time', FlightPosition.flight_id, FlightPosition.timestamp.desc())
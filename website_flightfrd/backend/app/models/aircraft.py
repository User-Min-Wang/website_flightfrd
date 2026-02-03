from extensions import db
from datetime import datetime
from sqlalchemy import UniqueConstraint


class Aircraft(db.Model):
    __tablename__ = 'aircraft'

    id = db.Column(db.Integer, primary_key=True)
    icao_code = db.Column(db.String(6), nullable=False, index=True)  # ICAO hex code
    registration = db.Column(db.String(10), unique=True)  # e.g., N12345
    airline = db.Column(db.String(100))  # Airline name
    model = db.Column(db.String(100))  # Aircraft model
    type_code = db.Column(db.String(10))  # IATA type code
    serial_number = db.Column(db.String(50))
    operator = db.Column(db.String(100))  # Operator/Owner
    built_date = db.Column(db.Date)  # Date of manufacture
    status = db.Column(db.String(20), default='active')  # active, retired, stored
    first_flight_date = db.Column(db.Date)  # First flight date
    registration_date = db.Column(db.Date)  # Registration date
    registration_expiry = db.Column(db.Date)  # Registration expiry date
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    flights = db.relationship('Flight', backref='aircraft', lazy=True, cascade='all, delete-orphan')
    images = db.relationship('Image', backref='aircraft', lazy=True, cascade='all, delete-orphan')

    __table_args__ = (
        UniqueConstraint('icao_code', name='unique_icao_code'),
    )

    def __repr__(self):
        return f'<Aircraft {self.icao_code} - {self.registration}>'

    def to_dict(self):
        """Convert aircraft object to dictionary representation"""
        return {
            'id': self.id,
            'icao_code': self.icao_code,
            'registration': self.registration,
            'airline': self.airline,
            'model': self.model,
            'type_code': self.type_code,
            'serial_number': self.serial_number,
            'operator': self.operator,
            'built_date': self.built_date.isoformat() if self.built_date else None,
            'status': self.status,
            'first_flight_date': self.first_flight_date.isoformat() if self.first_flight_date else None,
            'registration_date': self.registration_date.isoformat() if self.registration_date else None,
            'registration_expiry': self.registration_expiry.isoformat() if self.registration_expiry else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
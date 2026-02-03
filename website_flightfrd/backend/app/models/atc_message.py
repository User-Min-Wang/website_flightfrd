from extensions import db
from datetime import datetime


class ATCMessage(db.Model):
    __tablename__ = 'atc_messages'

    id = db.Column(db.Integer, primary_key=True)
    frequency = db.Column(db.String(10), nullable=False, index=True)  # e.g., 118.700
    callsign = db.Column(db.String(10), index=True)  # Aircraft or station callsign
    message_type = db.Column(db.String(50), nullable=False)  # clearance, contact, taxi, takeoff, landing, etc.
    message_content = db.Column(db.Text, nullable=False)  # The actual message content
    decoded_content = db.Column(db.Text)  # Decoded/interpreted message
    sender_type = db.Column(db.String(20))  # pilot, controller, station
    airport_code = db.Column(db.String(10), index=True)  # Associated airport ICAO code
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))  # Associated flight
    received_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)  # Time received
    processed_at = db.Column(db.DateTime)  # Time processed by system
    signal_strength = db.Column(db.Float)  # Signal strength if available
    modulation = db.Column(db.String(20))  # AM, FM, etc.
    channel = db.Column(db.String(20))  # Primary, backup, emergency
    is_emergency = db.Column(db.Boolean, default=False)  # Emergency communication
    priority_level = db.Column(db.Integer, default=1)  # Priority level (1-5)
    transcription_confidence = db.Column(db.Float)  # Confidence level of transcription
    verified = db.Column(db.Boolean, default=False)  # Whether message has been verified
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # User who verified
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ATCMessage {self.frequency} - {self.callsign}>'

    def to_dict(self):
        """Convert ATC message object to dictionary representation"""
        return {
            'id': self.id,
            'frequency': self.frequency,
            'callsign': self.callsign,
            'message_type': self.message_type,
            'message_content': self.message_content,
            'decoded_content': self.decoded_content,
            'sender_type': self.sender_type,
            'airport_code': self.airport_code,
            'flight_id': self.flight_id,
            'received_at': self.received_at.isoformat(),
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'signal_strength': self.signal_strength,
            'modulation': self.modulation,
            'channel': self.channel,
            'is_emergency': self.is_emergency,
            'priority_level': self.priority_level,
            'transcription_confidence': self.transcription_confidence,
            'verified': self.verified,
            'verified_by': self.verified_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
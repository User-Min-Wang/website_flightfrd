import logging
from datetime import datetime
from extensions import db
from app.models import ATCMessage, Flight, User


class ATCService:
    """
    Service class for handling ATC communication data
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def store_atc_message(self, frequency, callsign, message_content, message_type, 
                          sender_type=None, airport_code=None, flight_id=None, 
                          signal_strength=None, modulation=None, channel=None,
                          is_emergency=False, priority_level=1, transcription_confidence=None):
        """
        Store an ATC message in the database
        
        Args:
            frequency: Frequency of communication (e.g., 118.700)
            callsign: Callsign of aircraft or station
            message_content: Content of the message
            message_type: Type of message (clearance, contact, taxi, takeoff, landing, etc.)
            sender_type: Type of sender (pilot, controller, station)
            airport_code: Airport ICAO code
            flight_id: Associated flight ID
            signal_strength: Signal strength if available
            modulation: Modulation type (AM, FM, etc.)
            channel: Channel (Primary, backup, emergency)
            is_emergency: Whether this is an emergency communication
            priority_level: Priority level (1-5)
            transcription_confidence: Confidence level of transcription
            
        Returns:
            ATCMessage: Created ATC message object
        """
        try:
            # Validate and normalize inputs
            frequency = self._normalize_frequency(frequency)
            callsign = callsign.strip() if callsign else None
            
            # Create new ATC message
            atc_message = ATCMessage(
                frequency=frequency,
                callsign=callsign,
                message_type=message_type,
                message_content=message_content,
                sender_type=sender_type,
                airport_code=airport_code,
                flight_id=flight_id,
                signal_strength=signal_strength,
                modulation=modulation,
                channel=channel,
                is_emergency=is_emergency,
                priority_level=priority_level,
                transcription_confidence=transcription_confidence,
                received_at=datetime.utcnow()
            )
            
            # Add to database
            db.session.add(atc_message)
            db.session.commit()
            
            self.logger.info(f"Stored ATC message for frequency {frequency}, callsign {callsign}")
            
            return atc_message
            
        except Exception as e:
            self.logger.error(f"Error storing ATC message: {str(e)}")
            db.session.rollback()
            raise

    def _normalize_frequency(self, frequency):
        """
        Normalize frequency to standard format
        
        Args:
            frequency: Raw frequency value
            
        Returns:
            str: Normalized frequency
        """
        try:
            # Convert to float and then format to 3 decimal places
            freq_float = float(frequency)
            return f"{freq_float:.3f}"
        except (ValueError, TypeError):
            raise ValueError(f"Invalid frequency format: {frequency}")

    def get_recent_messages(self, limit=100, frequency=None, callsign=None, 
                            message_type=None, airport_code=None, flight_id=None):
        """
        Retrieve recent ATC messages with optional filters
        
        Args:
            limit: Maximum number of messages to return
            frequency: Filter by frequency
            callsign: Filter by callsign
            message_type: Filter by message type
            airport_code: Filter by airport code
            flight_id: Filter by flight ID
            
        Returns:
            list: List of ATC message objects
        """
        try:
            query = ATCMessage.query.order_by(ATCMessage.received_at.desc())
            
            if frequency:
                query = query.filter(ATCMessage.frequency == self._normalize_frequency(frequency))
            if callsign:
                query = query.filter(ATCMessage.callsign.ilike(f'%{callsign}%'))
            if message_type:
                query = query.filter(ATCMessage.message_type == message_type)
            if airport_code:
                query = query.filter(ATCMessage.airport_code == airport_code)
            if flight_id:
                query = query.filter(ATCMessage.flight_id == flight_id)
            
            messages = query.limit(limit).all()
            
            return messages
            
        except Exception as e:
            self.logger.error(f"Error retrieving ATC messages: {str(e)}")
            raise

    def decode_message(self, raw_message):
        """
        Decode/interpret raw ATC message content
        
        Args:
            raw_message: Raw message content
            
        Returns:
            str: Decoded/interpreted message
        """
        # This is a placeholder implementation
        # In a real application, this would involve complex parsing logic
        # possibly using ML models or rule-based systems
        decoded_content = raw_message.upper()  # Simple example transformation
        
        return decoded_content

    def mark_message_verified(self, message_id, verified_by_user_id):
        """
        Mark an ATC message as verified by a user
        
        Args:
            message_id: ID of the message to verify
            verified_by_user_id: ID of user verifying the message
            
        Returns:
            bool: Success status
        """
        try:
            message = ATCMessage.query.get(message_id)
            if not message:
                raise ValueError(f"ATC message with ID {message_id} not found")
            
            user = User.query.get(verified_by_user_id)
            if not user:
                raise ValueError(f"User with ID {verified_by_user_id} not found")
            
            message.verified = True
            message.verified_by = verified_by_user_id
            message.processed_at = datetime.utcnow()
            
            db.session.commit()
            
            self.logger.info(f"Marked ATC message {message_id} as verified by user {verified_by_user_id}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error marking ATC message as verified: {str(e)}")
            db.session.rollback()
            raise

    def get_messages_by_flight(self, flight_id, limit=50):
        """
        Retrieve ATC messages for a specific flight
        
        Args:
            flight_id: ID of flight
            limit: Maximum number of messages to return
            
        Returns:
            list: List of ATC message objects
        """
        try:
            messages = ATCMessage.query.filter_by(flight_id=flight_id)\
                                      .order_by(ATCMessage.received_at.desc())\
                                      .limit(limit)\
                                      .all()
            
            return messages
            
        except Exception as e:
            self.logger.error(f"Error retrieving ATC messages for flight {flight_id}: {str(e)}")
            raise

    def get_messages_by_airport(self, airport_code, limit=100):
        """
        Retrieve ATC messages for a specific airport
        
        Args:
            airport_code: ICAO code of airport
            limit: Maximum number of messages to return
            
        Returns:
            list: List of ATC message objects
        """
        try:
            messages = ATCMessage.query.filter_by(airport_code=airport_code)\
                                      .order_by(ATCMessage.received_at.desc())\
                                      .limit(limit)\
                                      .all()
            
            return messages
            
        except Exception as e:
            self.logger.error(f"Error retrieving ATC messages for airport {airport_code}: {str(e)}")
            raise
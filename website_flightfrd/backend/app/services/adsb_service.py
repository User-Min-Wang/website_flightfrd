import requests
import logging
from datetime import datetime, timedelta
from extensions import db, redis_client
from app.models import Aircraft, Flight
from app.utils.validators import validate_icao_code


class ADSBService:
    """
    Service class for handling ADS-B data retrieval and processing
    """
    
    def __init__(self):
        self.base_url = 'https://opensky-network.org/api'
        self.logger = logging.getLogger(__name__)
        
    def fetch_current_states(self, icao_codes=None):
        """
        Fetch current states of aircraft from ADS-B data
        
        Args:
            icao_codes: List of specific ICAO codes to fetch (optional)
            
        Returns:
            dict: Response from ADS-B API
        """
        try:
            # Build URL with optional icao codes filter
            url = f"{self.base_url}/states/all"
            params = {}
            
            if icao_codes:
                # Validate all ICAO codes before making request
                for code in icao_codes:
                    validate_icao_code(code)
                
                params['icao24'] = ','.join(icao_codes)
            
            # Make request to ADS-B API
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Process the data and update database
            self._process_states_data(data)
            
            return data
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching ADS-B states: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error in fetch_current_states: {str(e)}")
            raise

    def _process_states_data(self, data):
        """
        Process ADS-B states data and update database
        
        Args:
            data: Raw ADS-B states data
        """
        if 'states' not in data or not data['states']:
            return
            
        for state in data['states']:
            # Extract aircraft information
            icao_code = state[0].lower() if state[0] else None
            callsign = state[1].strip() if state[1] else None
            country = state[2] if state[2] else None
            latitude = state[6] if state[6] is not None else None
            longitude = state[5] if state[5] is not None else None
            altitude = state[7] if state[7] is not None else None
            velocity = state[9] if state[9] is not None else None
            heading = state[10] if state[10] is not None else None
            vertical_rate = state[11] if state[11] is not None else None
            on_ground = state[8] if state[8] is not None else None
            squawk = state[14] if state[14] else None
            baro_altitude = state[13] if state[13] is not None else None
            true_track = state[10] if state[10] is not None else None  # Same as heading in this case
            last_position_update = datetime.utcnow()  # Using current time as proxy for actual timestamp
            
            # Find or create aircraft record
            aircraft = Aircraft.query.filter_by(icao_code=icao_code).first()
            if not aircraft:
                aircraft = Aircraft(
                    icao_code=icao_code,
                    registration=callsign,
                    airline=country,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(aircraft)
                db.session.flush()  # Get ID without committing
            
            # Find or update flight record
            flight = Flight.query.filter_by(aircraft_id=aircraft.id).filter(Flight.status != 'landed').first()
            if not flight:
                flight = Flight(
                    aircraft_id=aircraft.id,
                    callsign=callsign,
                    origin_country=country,
                    status='active',
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(flight)
            else:
                # Update existing flight record
                flight.callsign = callsign
                flight.latitude = latitude
                flight.longitude = longitude
                flight.altitude = altitude
                flight.ground_speed = velocity
                flight.heading = heading
                flight.vertical_rate = vertical_rate
                flight.on_ground = on_ground
                flight.squawk = squawk
                flight.baro_altitude = baro_altitude
                flight.true_track = true_track
                flight.last_position_update = last_position_update
                flight.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Cache the data for quick retrieval
            self._cache_flight_data(flight)

    def _cache_flight_data(self, flight):
        """
        Cache flight data in Redis for quick retrieval
        
        Args:
            flight: Flight object to cache
        """
        try:
            # Create cache key
            cache_key = f"flight:{flight.id}"
            
            # Prepare data to cache
            flight_data = {
                'id': flight.id,
                'flight_number': flight.flight_number,
                'callsign': flight.callsign,
                'aircraft_id': flight.aircraft_id,
                'latitude': flight.latitude,
                'longitude': flight.longitude,
                'altitude': flight.altitude,
                'ground_speed': flight.ground_speed,
                'heading': flight.heading,
                'on_ground': flight.on_ground,
                'squawk': flight.squawk,
                'status': flight.status,
                'last_position_update': flight.last_position_update.isoformat() if flight.last_position_update else None
            }
            
            # Store in Redis with expiration (10 minutes)
            redis_client.setex(cache_key, 600, str(flight_data))
            
        except Exception as e:
            self.logger.error(f"Error caching flight data: {str(e)}")

    def get_cached_flight(self, flight_id):
        """
        Retrieve cached flight data from Redis
        
        Args:
            flight_id: ID of flight to retrieve
            
        Returns:
            dict: Cached flight data or None if not found
        """
        try:
            cache_key = f"flight:{flight_id}"
            cached_data = redis_client.get(cache_key)
            
            if cached_data:
                return eval(cached_data.decode('utf-8'))
                
            return None
            
        except Exception as e:
            self.logger.error(f"Error retrieving cached flight data: {str(e)}")
            return None

    def fetch_historical_data(self, icao_code, start_time, end_time):
        """
        Fetch historical flight data for a specific aircraft
        
        Args:
            icao_code: ICAO code of aircraft
            start_time: Start time for historical data
            end_time: End time for historical data
            
        Returns:
            dict: Historical flight data
        """
        validate_icao_code(icao_code)
        
        try:
            # Convert times to timestamps
            start_timestamp = int(start_time.timestamp())
            end_timestamp = int(end_time.timestamp())
            
            # Make request to historical ADS-B API
            url = f"{self.base_url}/tracks/all"
            params = {
                'icao24': icao_code.lower(),
                'start': start_timestamp,
                'end': end_timestamp
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching historical ADS-B data: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error in fetch_historical_data: {str(e)}")
            raise
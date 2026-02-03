import re


def validate_icao_code(icao_code):
    """
    Validate ICAO code format
    
    Args:
        icao_code: ICAO code to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not icao_code or len(icao_code) != 6:
        return False
    
    # ICAO codes are hexadecimal characters only
    return bool(re.match(r'^[0-9A-Fa-f]{6}$', icao_code))


def validate_flight_number(flight_number):
    """
    Validate flight number format
    
    Args:
        flight_number: Flight number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not flight_number:
        return False
    
    # Flight numbers typically have 2-3 letter airline code followed by numbers
    return bool(re.match(r'^[A-Za-z]{2,3}\d+$', flight_number))


def validate_callsign(callsign):
    """
    Validate radio callsign format
    
    Args:
        callsign: Callsign to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not callsign:
        return False
    
    # Callsigns are typically 3-7 alphanumeric characters
    return bool(re.match(r'^[A-Za-z0-9]{3,7}$', callsign))


def validate_airport_code(airport_code):
    """
    Validate airport code (ICAO or IATA)
    
    Args:
        airport_code: Airport code to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not airport_code:
        return False
    
    # ICAO codes are 4 letters, IATA codes are 3 letters
    return bool(re.match(r'^[A-Za-z]{3,4}$', airport_code))


def validate_email(email):
    """
    Validate email address format
    
    Args:
        email: Email to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_registration(registration):
    """
    Validate aircraft registration format
    
    Args:
        registration: Registration to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not registration:
        return False
    
    # Aircraft registrations vary by country but usually start with a prefix like N, G, F, D, etc.
    # followed by 1-5 alphanumeric characters
    return bool(re.match(r'^[A-Za-z][A-Za-z0-9]{1,5}$', registration))


def validate_squawk_code(squawk_code):
    """
    Validate transponder squawk code
    
    Args:
        squawk_code: Squawk code to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not squawk_code:
        return False
    
    # Squawk codes are 4-digit octal numbers (digits 0-7 only)
    return bool(re.match(r'^[0-7]{4}$', squawk_code))


def validate_coordinates(latitude, longitude):
    """
    Validate latitude and longitude coordinates
    
    Args:
        latitude: Latitude to validate
        longitude: Longitude to validate
        
    Returns:
        bool: True if both valid, False otherwise
    """
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        return -90 <= lat <= 90 and -180 <= lon <= 180
    except (TypeError, ValueError):
        return False
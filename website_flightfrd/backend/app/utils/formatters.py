from datetime import datetime


def format_datetime(dt, format_string='%Y-%m-%d %H:%M:%S'):
    """
    Format a datetime object to a string
    
    Args:
        dt: datetime object to format
        format_string: Format string to use
        
    Returns:
        str: Formatted datetime string
    """
    if dt is None:
        return None
    return dt.strftime(format_string)


def format_duration(seconds):
    """
    Format duration in seconds to human-readable format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        str: Formatted duration string
    """
    if seconds is None:
        return None
    
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def format_distance(distance_meters, unit='km'):
    """
    Format distance in meters to specified unit
    
    Args:
        distance_meters: Distance in meters
        unit: Unit to convert to ('km', 'nm', 'mi')
        
    Returns:
        float: Formatted distance
    """
    if distance_meters is None:
        return None
    
    # Conversion factors to kilometers
    conversion_factors = {
        'km': 1.0,           # kilometers
        'nm': 0.539957,      # nautical miles
        'mi': 0.621371       # statute miles
    }
    
    if unit not in conversion_factors:
        raise ValueError(f"Unsupported unit: {unit}. Use one of {list(conversion_factors.keys())}")
    
    return round(distance_meters * conversion_factors[unit] / 1000.0, 2)


def format_altitude(altitude_feet, unit='feet'):
    """
    Format altitude to specified unit
    
    Args:
        altitude_feet: Altitude in feet
        unit: Unit to convert to ('feet', 'meters')
        
    Returns:
        float: Formatted altitude
    """
    if altitude_feet is None:
        return None
    
    if unit == 'feet':
        return int(altitude_feet)
    elif unit == 'meters':
        return int(altitude_feet * 0.3048)
    else:
        raise ValueError(f"Unsupported unit: {unit}. Use 'feet' or 'meters'")


def format_speed(speed_knots, unit='knots'):
    """
    Format speed to specified unit
    
    Args:
        speed_knots: Speed in knots
        unit: Unit to convert to ('knots', 'kmh', 'mph')
        
    Returns:
        float: Formatted speed
    """
    if speed_knots is None:
        return None
    
    # Conversion factors from knots
    conversion_factors = {
        'knots': 1.0,        # knots
        'kmh': 1.852,        # kilometers per hour
        'mph': 1.15078       # miles per hour
    }
    
    if unit not in conversion_factors:
        raise ValueError(f"Unsupported unit: {unit}. Use one of {list(conversion_factors.keys())}")
    
    return round(speed_knots * conversion_factors[unit], 2)


def format_heading(heading_degrees):
    """
    Format heading in degrees to compass direction
    
    Args:
        heading_degrees: Heading in degrees (0-360)
        
    Returns:
        str: Compass direction
    """
    if heading_degrees is None:
        return None
    
    # Normalize to 0-360 range
    heading = heading_degrees % 360
    
    directions = [
        'N', 'NNE', 'NE', 'ENE', 
        'E', 'ESE', 'SE', 'SSE',
        'S', 'SSW', 'SW', 'WSW',
        'W', 'WNW', 'NW', 'NNW'
    ]
    
    index = round(heading / (360 / len(directions))) % len(directions)
    return directions[index]


def format_file_size(size_bytes):
    """
    Format file size in bytes to human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        str: Human-readable file size
    """
    if size_bytes is None:
        return None
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.2f} PB"


def format_icao_code(icao_code):
    """
    Format ICAO code to uppercase
    
    Args:
        icao_code: ICAO code to format
        
    Returns:
        str: Uppercase ICAO code
    """
    if icao_code is None:
        return None
    return icao_code.upper()


def format_registration(registration):
    """
    Format aircraft registration with proper spacing/prefix
    
    Args:
        registration: Aircraft registration
        
    Returns:
        str: Formatted registration
    """
    if registration is None:
        return None
    
    # Standardize registration formatting
    reg = registration.strip().upper()
    
    # Add hyphen for certain formats (e.g., N-numbers don't need it, but others might)
    if reg.startswith('N') and reg[1:].isdigit():
        return reg  # N-number format (e.g., N12345)
    else:
        return reg
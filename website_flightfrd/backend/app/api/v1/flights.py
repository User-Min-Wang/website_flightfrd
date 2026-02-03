from flask import jsonify, request
from app.api.v1 import bp
from app.models import Flight, Aircraft
from app.schemas import FlightSchema
from app.services import ADSBService
from extensions import db


adsb_service = ADSBService()


@bp.route('/flights', methods=['GET'])
def get_flights_list():
    """Get a paginated list of flights"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', '', type=str)
    aircraft_id = request.args.get('aircraft_id', type=int)
    departure_airport = request.args.get('departure_airport', '', type=str)
    arrival_airport = request.args.get('arrival_airport', '', type=str)
    
    # Build query
    query = Flight.query
    
    if status:
        query = query.filter(Flight.status == status)
    if aircraft_id:
        query = query.filter(Flight.aircraft_id == aircraft_id)
    if departure_airport:
        query = query.filter(Flight.departure_airport == departure_airport)
    if arrival_airport:
        query = query.filter(Flight.arrival_airport == arrival_airport)
    
    # Join with aircraft to enable searching
    query = query.join(Aircraft)
    
    # Paginate results
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    flights = pagination.items
    
    return jsonify({
        'flights': [flight.to_dict() for flight in flights],
        'pagination': {
            'page': page,
            'pages': pagination.pages,
            'total': pagination.total,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    })


@bp.route('/flights/<int:flight_id>', methods=['GET'])
def get_flight_detail(flight_id):
    """Get detailed information about a specific flight"""
    flight = Flight.query.get_or_404(flight_id)
    return jsonify(flight.to_dict())


@bp.route('/flights', methods=['POST'])
def create_flight():
    """Create a new flight record"""
    try:
        # Validate input data
        schema = FlightSchema()
        data = schema.load(request.json)
        
        # Verify aircraft exists
        aircraft = Aircraft.query.get(data['aircraft_id'])
        if not aircraft:
            return jsonify({'error': 'Aircraft not found'}), 404
        
        # Create new flight
        flight = Flight(**data)
        db.session.add(flight)
        db.session.commit()
        
        return jsonify(flight.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@bp.route('/flights/<int:flight_id>', methods=['PUT'])
def update_flight(flight_id):
    """Update an existing flight record"""
    flight = Flight.query.get_or_404(flight_id)
    
    try:
        # Validate input data
        schema = FlightSchema()
        data = schema.load(request.json, partial=True)
        
        # Update flight fields
        for field, value in data.items():
            setattr(flight, field, value)
        
        db.session.commit()
        
        return jsonify(flight.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@bp.route('/flights/<int:flight_id>', methods=['DELETE'])
def delete_flight(flight_id):
    """Delete a flight record"""
    flight = Flight.query.get_or_404(flight_id)
    
    db.session.delete(flight)
    db.session.commit()
    
    return jsonify({'message': 'Flight deleted successfully'})


@bp.route('/flights/search', methods=['GET'])
def search_flights():
    """Search for flights based on various criteria"""
    departure_airport = request.args.get('departure_airport', '', type=str)
    arrival_airport = request.args.get('arrival_airport', '', type=str)
    date = request.args.get('date', '', type=str)  # Format: YYYY-MM-DD
    callsign = request.args.get('callsign', '', type=str)
    
    # Build query
    query = Flight.query
    
    if departure_airport:
        query = query.filter(Flight.departure_airport == departure_airport.upper())
    if arrival_airport:
        query = query.filter(Flight.arrival_airport == arrival_airport.upper())
    if date:
        # Filter by date (convert string to date object)
        from datetime import datetime
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            query = query.filter(
                db.func.date(Flight.departure_time) == date_obj
            )
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400
    if callsign:
        query = query.filter(Flight.callsign.ilike(f'%{callsign}%'))
    
    # Execute query with limit
    limit = request.args.get('limit', 50, type=int)
    flights = query.limit(limit).all()
    
    return jsonify({
        'flights': [flight.to_dict() for flight in flights],
        'count': len(flights)
    })


@bp.route('/flights/active', methods=['GET'])
def get_active_flights():
    """Get all currently active flights"""
    # Get active flights (not landed or cancelled)
    active_flights = Flight.query.filter(
        Flight.status.in_(['active', 'scheduled'])
    ).all()
    
    return jsonify({
        'flights': [flight.to_dict() for flight in active_flights],
        'count': len(active_flights)
    })


@bp.route('/flights/<string:icao_code>/positions', methods=['GET'])
def get_flight_positions(icao_code):
    """Get position history for a flight identified by ICAO code"""
    from app.models import FlightPosition
    
    # Get the flight by ICAO code through its aircraft
    flight = Flight.query.join(Aircraft).filter(Aircraft.icao_code == icao_code).first_or_404()
    
    # Get position history
    positions = FlightPosition.query.filter_by(flight_id=flight.id).all()
    
    return jsonify({
        'flight_id': flight.id,
        'positions': [pos.to_dict() for pos in positions],
        'count': len(positions)
    })
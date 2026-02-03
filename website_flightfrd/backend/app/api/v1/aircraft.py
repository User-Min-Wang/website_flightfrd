from flask import jsonify, request
from app.api.v1 import bp
from app.models import Aircraft, Flight
from app.schemas import AircraftSchema
from app.services import ADSBService
from extensions import db


adsb_service = ADSBService()


@bp.route('/aircraft', methods=['GET'])
def get_aircraft_list():
    """Get a paginated list of aircraft"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)
    
    # Build query
    query = Aircraft.query
    
    if search:
        query = query.filter(
            db.or_(
                Aircraft.registration.contains(search),
                Aircraft.model.contains(search),
                Aircraft.icao_code.contains(search)
            )
        )
    
    # Paginate results
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    aircraft_list = pagination.items
    
    return jsonify({
        'aircraft': [aircraft.to_dict() for aircraft in aircraft_list],
        'pagination': {
            'page': page,
            'pages': pagination.pages,
            'total': pagination.total,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    })


@bp.route('/aircraft/<int:aircraft_id>', methods=['GET'])
def get_aircraft_detail(aircraft_id):
    """Get detailed information about a specific aircraft"""
    aircraft = Aircraft.query.get_or_404(aircraft_id)
    return jsonify(aircraft.to_dict())


@bp.route('/aircraft', methods=['POST'])
def create_aircraft():
    """Create a new aircraft record"""
    try:
        # Validate input data
        schema = AircraftSchema()
        data = schema.load(request.json)
        
        # Check if aircraft already exists
        existing_aircraft = Aircraft.query.filter_by(icao_code=data['icao_code']).first()
        if existing_aircraft:
            return jsonify({'error': 'Aircraft with this ICAO code already exists'}), 400
        
        # Create new aircraft
        aircraft = Aircraft(**data)
        db.session.add(aircraft)
        db.session.commit()
        
        return jsonify(aircraft.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@bp.route('/aircraft/<int:aircraft_id>', methods=['PUT'])
def update_aircraft(aircraft_id):
    """Update an existing aircraft record"""
    aircraft = Aircraft.query.get_or_404(aircraft_id)
    
    try:
        # Validate input data
        schema = AircraftSchema()
        data = schema.load(request.json, partial=True)
        
        # Update aircraft fields
        for field, value in data.items():
            setattr(aircraft, field, value)
        
        db.session.commit()
        
        return jsonify(aircraft.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@bp.route('/aircraft/<int:aircraft_id>', methods=['DELETE'])
def delete_aircraft(aircraft_id):
    """Delete an aircraft record"""
    aircraft = Aircraft.query.get_or_404(aircraft_id)
    
    # Check if aircraft has associated flights
    flight_count = Flight.query.filter_by(aircraft_id=aircraft_id).count()
    if flight_count > 0:
        return jsonify({'error': 'Cannot delete aircraft with associated flights'}), 400
    
    db.session.delete(aircraft)
    db.session.commit()
    
    return jsonify({'message': 'Aircraft deleted successfully'})


@bp.route('/aircraft/<string:icao_code>/fetch', methods=['POST'])
def fetch_aircraft_data(icao_code):
    """Fetch live data for a specific aircraft from ADS-B"""
    try:
        # Validate ICAO code format
        if len(icao_code) != 6:
            return jsonify({'error': 'ICAO code must be 6 characters'}), 400
        
        # Fetch data from ADS-B service
        result = adsb_service.fetch_current_states([icao_code])
        
        # Return the state data
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/aircraft/<int:aircraft_id>/flights', methods=['GET'])
def get_aircraft_flights(aircraft_id):
    """Get all flights for a specific aircraft"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    aircraft = Aircraft.query.get_or_404(aircraft_id)
    
    # Get flights for this aircraft
    pagination = Flight.query.filter_by(aircraft_id=aircraft_id)\
                             .paginate(page=page, per_page=per_page, error_out=False)
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
from flask import jsonify, request
from app.api.v1 import bp
from app.models import User, Aircraft
from app.services import CalendarService
from extensions import db
from datetime import datetime


calendar_service = CalendarService()


@bp.route('/calendar/bookings', methods=['GET'])
def get_bookings():
    """Get a list of bookings with optional filtering"""
    user_id = request.args.get('user_id', type=int)
    aircraft_id = request.args.get('aircraft_id', type=int)
    status = request.args.get('status', '', type=str)
    limit = request.args.get('limit', default=50, type=int)
    
    # Validate user exists if provided
    if user_id:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
    
    # Validate aircraft exists if provided
    if aircraft_id:
        aircraft = Aircraft.query.get(aircraft_id)
        if not aircraft:
            return jsonify({'error': 'Aircraft not found'}), 404
    
    # Get bookings based on filters
    if user_id:
        bookings = calendar_service.get_user_bookings(user_id, status_filter=status, limit=limit)
    elif aircraft_id:
        # For aircraft bookings, we'd need to implement a method in the service
        # For now, returning an empty list as placeholder
        bookings = []
    else:
        # If no filters provided, return error since we need at least one filter
        return jsonify({'error': 'Either user_id or aircraft_id must be provided'}), 400
    
    return jsonify({
        'bookings': bookings,
        'count': len(bookings)
    })


@bp.route('/calendar/bookings', methods=['POST'])
def create_booking():
    """Create a new booking"""
    try:
        data = request.json or {}
        
        # Required fields
        user_id = data.get('user_id')
        aircraft_id = data.get('aircraft_id')
        start_time_str = data.get('start_time')
        end_time_str = data.get('end_time')
        
        if not all([user_id, aircraft_id, start_time_str, end_time_str]):
            return jsonify({'error': 'Missing required fields: user_id, aircraft_id, start_time, end_time'}), 400
        
        # Validate user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Validate aircraft exists
        aircraft = Aircraft.query.get(aircraft_id)
        if not aircraft:
            return jsonify({'error': 'Aircraft not found'}), 404
        
        # Parse datetime strings
        try:
            start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid datetime format. Use ISO format.'}), 400
        
        # Optional fields
        purpose = data.get('purpose', '')
        status = data.get('status', 'pending')
        
        # Create booking using the service
        booking = calendar_service.create_booking(
            user_id=user_id,
            aircraft_id=aircraft_id,
            start_time=start_time,
            end_time=end_time,
            purpose=purpose,
            status=status
        )
        
        return jsonify(booking), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/calendar/aircraft/<int:aircraft_id>/schedule', methods=['GET'])
def get_aircraft_schedule(aircraft_id):
    """Get the schedule for a specific aircraft"""
    # Validate aircraft exists
    aircraft = Aircraft.query.get_or_404(aircraft_id)
    
    # Get date range from query parameters
    start_date_str = request.args.get('start_date', type=str)
    end_date_str = request.args.get('end_date', type=str)
    
    if not all([start_date_str, end_date_str]):
        return jsonify({'error': 'Both start_date and end_date are required. Use YYYY-MM-DD format.'}), 400
    
    try:
        from datetime import datetime
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD format.'}), 400
    
    # Get schedule using the service
    schedule = calendar_service.get_aircraft_schedule(aircraft_id, start_date, end_date)
    
    return jsonify({
        'aircraft_id': aircraft_id,
        'schedule': schedule,
        'count': len(schedule),
        'period': {
            'start_date': start_date_str,
            'end_date': end_date_str
        }
    })


@bp.route('/calendar/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    """Update an existing booking"""
    try:
        data = request.json or {}
        
        # Allowable updates
        new_status = data.get('status')
        user_id = data.get('user_id')  # For permission checks
        
        if new_status:
            # Update status using the service
            success = calendar_service.update_booking_status(booking_id, new_status, user_id)
            
            if not success:
                return jsonify({'error': 'Failed to update booking status'}), 500
        
        # Return updated booking info (placeholder implementation)
        # In a real implementation, we would fetch the updated booking from DB
        return jsonify({
            'message': 'Booking updated successfully',
            'booking_id': booking_id,
            'status': new_status
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/calendar/bookings/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    """Cancel a booking"""
    try:
        user_id = request.json.get('user_id') if request.json else None
        
        # Cancel booking using the service
        success = calendar_service.cancel_booking(booking_id, user_id)
        
        if success:
            return jsonify({'message': 'Booking cancelled successfully'})
        else:
            return jsonify({'error': 'Failed to cancel booking'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/calendar/check_availability', methods=['POST'])
def check_availability():
    """Check if an aircraft is available for booking in a given time slot"""
    try:
        data = request.json or {}
        
        aircraft_id = data.get('aircraft_id')
        start_time_str = data.get('start_time')
        end_time_str = data.get('end_time')
        
        if not all([aircraft_id, start_time_str, end_time_str]):
            return jsonify({'error': 'Missing required fields: aircraft_id, start_time, end_time'}), 400
        
        # Validate aircraft exists
        aircraft = Aircraft.query.get(aircraft_id)
        if not aircraft:
            return jsonify({'error': 'Aircraft not found'}), 404
        
        # Parse datetime strings
        try:
            start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid datetime format. Use ISO format.'}), 400
        
        # Check for conflicts using the service
        conflict_exists = calendar_service.check_booking_conflict(aircraft_id, start_time, end_time)
        
        return jsonify({
            'available': not conflict_exists,
            'conflict_exists': conflict_exists,
            'requested_period': {
                'start_time': start_time_str,
                'end_time': end_time_str
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
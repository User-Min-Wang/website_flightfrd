from flask import jsonify, request
from flask_socketio import emit, join_room, leave_room
from app.api.v1 import bp
from app.models import ATCMessage, Flight, User
from app.services import ATCService
from extensions import db, socketio


atc_service = ATCService()


@bp.route('/atc/messages', methods=['GET'])
def get_atc_messages():
    """Get a paginated list of ATC messages"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    frequency = request.args.get('frequency', '', type=str)
    callsign = request.args.get('callsign', '', type=str)
    message_type = request.args.get('message_type', '', type=str)
    airport_code = request.args.get('airport_code', '', type=str)
    flight_id = request.args.get('flight_id', type=int)
    
    # Get messages using the service
    messages = atc_service.get_recent_messages(
        limit=per_page,
        frequency=frequency,
        callsign=callsign,
        message_type=message_type,
        airport_code=airport_code,
        flight_id=flight_id
    )
    
    # Calculate pagination info
    total = len(messages)
    pages = (total + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_messages = messages[start_idx:end_idx]
    
    return jsonify({
        'messages': [msg.to_dict() for msg in paginated_messages],
        'pagination': {
            'page': page,
            'pages': pages,
            'total': total,
            'has_next': page < pages,
            'has_prev': page > 1
        }
    })


@bp.route('/atc/messages', methods=['POST'])
def create_atc_message():
    """Create a new ATC message"""
    try:
        data = request.json or {}
        
        # Required fields
        frequency = data.get('frequency')
        callsign = data.get('callsign')
        message_content = data.get('message_content')
        message_type = data.get('message_type')
        
        if not all([frequency, callsign, message_content, message_type]):
            return jsonify({'error': 'Missing required fields: frequency, callsign, message_content, message_type'}), 400
        
        # Optional fields
        sender_type = data.get('sender_type')
        airport_code = data.get('airport_code')
        flight_id = data.get('flight_id')
        signal_strength = data.get('signal_strength')
        modulation = data.get('modulation')
        channel = data.get('channel')
        is_emergency = data.get('is_emergency', False)
        priority_level = data.get('priority_level', 1)
        transcription_confidence = data.get('transcription_confidence')
        
        # Create message using the service
        message = atc_service.store_atc_message(
            frequency=frequency,
            callsign=callsign,
            message_content=message_content,
            message_type=message_type,
            sender_type=sender_type,
            airport_code=airport_code,
            flight_id=flight_id,
            signal_strength=signal_strength,
            modulation=modulation,
            channel=channel,
            is_emergency=is_emergency,
            priority_level=priority_level,
            transcription_confidence=transcription_confidence
        )
        
        # Emit to WebSocket clients
        socketio.emit('new_atc_message', message.to_dict(), namespace='/atc')
        
        return jsonify(message.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/atc/messages/<int:message_id>', methods=['GET'])
def get_atc_message_detail(message_id):
    """Get detailed information about a specific ATC message"""
    message = ATCMessage.query.get_or_404(message_id)
    return jsonify(message.to_dict())


@bp.route('/atc/messages/<int:message_id>', methods=['PUT'])
def update_atc_message(message_id):
    """Update an existing ATC message"""
    message = ATCMessage.query.get_or_404(message_id)
    
    try:
        data = request.json or {}
        
        # Update allowed fields
        if 'decoded_content' in data:
            message.decoded_content = data['decoded_content']
        if 'verified' in data:
            message.verified = data['verified']
        if 'priority_level' in data:
            message.priority_level = data['priority_level']
        
        db.session.commit()
        
        return jsonify(message.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@bp.route('/atc/messages/<int:message_id>/verify', methods=['POST'])
def verify_atc_message(message_id):
    """Mark an ATC message as verified"""
    try:
        data = request.json or {}
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        # Verify the message
        success = atc_service.mark_message_verified(message_id, user_id)
        
        if success:
            message = ATCMessage.query.get_or_404(message_id)
            # Emit to WebSocket clients
            socketio.emit('atc_message_verified', message.to_dict(), namespace='/atc')
            return jsonify(message.to_dict())
        else:
            return jsonify({'error': 'Failed to verify message'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/atc/flight/<int:flight_id>/messages', methods=['GET'])
def get_flight_atc_messages(flight_id):
    """Get all ATC messages for a specific flight"""
    # Validate flight exists
    flight = Flight.query.get_or_404(flight_id)
    
    # Get messages using the service
    messages = atc_service.get_messages_by_flight(flight_id)
    
    return jsonify({
        'messages': [msg.to_dict() for msg in messages],
        'count': len(messages)
    })


@bp.route('/atc/airport/<airport_code>/messages', methods=['GET'])
def get_airport_atc_messages(airport_code):
    """Get all ATC messages for a specific airport"""
    # Get messages using the service
    messages = atc_service.get_messages_by_airport(airport_code)
    
    return jsonify({
        'messages': [msg.to_dict() for msg in messages],
        'count': len(messages),
        'airport_code': airport_code
    })


# WebSocket events for ATC communication
@socketio.on('connect', namespace='/atc')
def handle_atc_connect():
    """Handle client connection to ATC namespace"""
    print('Client connected to ATC stream')
    emit('connected', {'message': 'Connected to ATC communication stream'})


@socketio.on('disconnect', namespace='/atc')
def handle_atc_disconnect():
    """Handle client disconnection from ATC namespace"""
    print('Client disconnected from ATC stream')


@socketio.on('subscribe_to_frequency', namespace='/atc')
def handle_subscribe_frequency(data):
    """Handle subscription to a specific frequency"""
    frequency = data.get('frequency')
    if frequency:
        # Add client to room for this frequency
        join_room(frequency, namespace='/atc')
        emit('subscribed', {'frequency': frequency})


@socketio.on('unsubscribe_from_frequency', namespace='/atc')
def handle_unsubscribe_frequency(data):
    """Handle unsubscription from a specific frequency"""
    frequency = data.get('frequency')
    if frequency:
        # Remove client from room for this frequency
        leave_room(frequency, namespace='/atc')
        emit('unsubscribed', {'frequency': frequency})
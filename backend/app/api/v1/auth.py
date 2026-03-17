from flask import Blueprint, request, jsonify
from extensions import db
from app.models.user import User
from app.schemas.user_schema import UserSchema, LoginSchema, RegisterSchema
from datetime import datetime
import jwt
from config import Config
from app.utils.email_service import generate_verification_token, send_verification_email

# Create blueprint for authentication
bp = Blueprint('auth', __name__, url_prefix='/auth')

user_schema = UserSchema()
login_schema = LoginSchema()
register_schema = RegisterSchema()


@bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate input
    errors = register_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
    # Check if username or email already exists
    existing_user = User.query.filter(
        (User.username == data['username']) | (User.email == data['email'])
    ).first()
    
    if existing_user:
        return jsonify({'error': 'Username or email already exists'}), 400
    
    # Create new user (not verified yet)
    user = User(
        username=data['username'],
        email=data['email'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        is_verified=False  # Email not verified yet
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Generate email verification token
    try:
        token = generate_verification_token(user.email)
        send_verification_email(user.email, user.username, token)
    except Exception as e:
        # Log error but don't fail registration
        print(f"Failed to send verification email: {str(e)}")
    
    # Generate JWT token (limited access until verified)
    auth_token = jwt.encode(
        {'user_id': user.id, 'username': user.username},
        Config.JWT_SECRET_KEY,
        algorithm='HS256'
    )
    
    return jsonify({
        'message': 'User registered successfully. Please check your email to verify your account.',
        'token': auth_token,
        'user': user.to_dict(),
        'requires_verification': True
    }), 201


@bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    """Verify user's email address"""
    from app.utils.email_service import verify_verification_token
    
    email = verify_verification_token(token, expiration=Config.EMAIL_VERIFICATION_TOKEN_EXPIRES.total_seconds())
    
    if not email:
        return jsonify({'error': 'Invalid or expired verification token'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if user.is_verified:
        return jsonify({'message': 'Email already verified', 'user': user.to_dict()}), 200
    
    user.is_verified = True
    db.session.commit()
    
    return jsonify({
        'message': 'Email verified successfully',
        'user': user.to_dict()
    }), 200


@bp.route('/resend-verification', methods=['POST'])
def resend_verification():
    """Resend verification email"""
    data = request.get_json()
    
    if not data or 'email' not in data:
        return jsonify({'error': 'Email is required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'error': 'User not found with this email'}), 404
    
    if user.is_verified:
        return jsonify({'message': 'Email already verified'}), 200
    
    try:
        token = generate_verification_token(user.email)
        send_verification_email(user.email, user.username, token)
        return jsonify({'message': 'Verification email sent'}), 200
    except Exception as e:
        print(f"Failed to send verification email: {str(e)}")
        return jsonify({'error': 'Failed to send verification email'}), 500


@bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token"""
    data = request.get_json()
    
    # Validate input
    errors = login_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
    # Find user by username or email
    user = User.query.filter(
        (User.username == data['identity']) | (User.email == data['identity'])
    ).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username/email or password'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 403
    
    # Update last login and login count
    user.last_login = datetime.utcnow()
    user.login_count += 1
    db.session.commit()
    
    # Generate JWT token
    token = jwt.encode(
        {'user_id': user.id, 'username': user.username, 'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES},
        Config.JWT_SECRET_KEY,
        algorithm='HS256'
    )
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()
    }), 200


@bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current authenticated user information"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not token:
        return jsonify({'error': 'Token is required'}), 401
    
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        user = User.query.get(payload['user_id'])
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401


@bp.route('/logout', methods=['POST'])
def logout():
    """Logout user (client should remove token)"""
    # In a stateless JWT system, logout is handled client-side
    # by removing the token from storage
    return jsonify({'message': 'Logout successful'}), 200

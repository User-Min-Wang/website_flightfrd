from flask import jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
import os
from app.api.v1 import bp
from app.models import Image, Aircraft, User
from app.services import ImageService
from extensions import db


# Initialize image service with upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'app/static/uploads')
image_service = ImageService(upload_folder=UPLOAD_FOLDER)


@bp.route('/images', methods=['GET'])
def get_images_list():
    """Get a paginated list of images"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    aircraft_id = request.args.get('aircraft_id', type=int)
    approved = request.args.get('approved', type=bool)
    
    # Build query
    query = Image.query
    
    if aircraft_id:
        query = query.filter(Image.aircraft_id == aircraft_id)
    if approved is not None:
        query = query.filter(Image.approved == approved)
    
    # Paginate results
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    images = pagination.items
    
    return jsonify({
        'images': [image.to_dict() for image in images],
        'pagination': {
            'page': page,
            'pages': pagination.pages,
            'total': pagination.total,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    })


@bp.route('/images/<int:image_id>', methods=['GET'])
def get_image_detail(image_id):
    """Get detailed information about a specific image"""
    image = Image.query.get_or_404(image_id)
    return jsonify(image.to_dict())


@bp.route('/images/upload', methods=['POST'])
def upload_image():
    """Upload a new image for an aircraft"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get required form data
        aircraft_id = request.form.get('aircraft_id', type=int)
        if not aircraft_id:
            return jsonify({'error': 'Aircraft ID is required'}), 400
        
        # Optional form data
        user_id = request.form.get('user_id', type=int)
        description = request.form.get('description', '')
        image_type = request.form.get('image_type', 'photo')
        license = request.form.get('license', 'copyright')
        
        # Validate aircraft exists
        aircraft = Aircraft.query.get(aircraft_id)
        if not aircraft:
            return jsonify({'error': 'Aircraft not found'}), 404
        
        # Upload image using service
        image_record = image_service.save_image(
            file=file,
            aircraft_id=aircraft_id,
            user_id=user_id,
            description=description,
            image_type=image_type,
            license=license
        )
        
        return jsonify(image_record.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/images/<int:image_id>', methods=['PUT'])
def update_image(image_id):
    """Update an existing image record"""
    image = Image.query.get_or_404(image_id)
    
    try:
        # Get data from request
        data = request.json or {}
        
        # Update allowed fields
        if 'description' in data:
            image.description = data['description']
        if 'image_type' in data:
            image.image_type = data['image_type']
        if 'license' in data:
            image.license = data['license']
        if 'is_featured' in data:
            image.is_featured = data['is_featured']
        
        db.session.commit()
        
        return jsonify(image.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@bp.route('/images/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    """Delete an image record"""
    try:
        success = image_service.delete_image(image_id)
        
        if success:
            return jsonify({'message': 'Image deleted successfully'})
        else:
            return jsonify({'error': 'Failed to delete image'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/images/<int:image_id>/approve', methods=['POST'])
def approve_image(image_id):
    """Approve an image for public display"""
    try:
        # Get user ID from request
        data = request.json or {}
        approver_id = data.get('approver_id')
        
        if not approver_id:
            return jsonify({'error': 'Approver ID is required'}), 400
        
        # Validate user exists
        user = User.query.get(approver_id)
        if not user:
            return jsonify({'error': 'Approver not found'}), 404
        
        # Check if user has permission to approve
        if user.role not in ['admin', 'moderator']:
            return jsonify({'error': 'Insufficient permissions to approve images'}), 403
        
        # Approve image
        success = image_service.approve_image(image_id, approver_id)
        
        if success:
            image = Image.query.get_or_404(image_id)
            return jsonify(image.to_dict())
        else:
            return jsonify({'error': 'Failed to approve image'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/images/<int:image_id>/feature', methods=['POST'])
def set_featured_image(image_id):
    """Set an image as the featured image for an aircraft"""
    try:
        # Get image to ensure it exists
        image = Image.query.get_or_404(image_id)
        
        # Set as featured
        success = image_service.set_featured_image(image_id, image.aircraft_id)
        
        if success:
            return jsonify({'message': 'Featured image set successfully'})
        else:
            return jsonify({'error': 'Failed to set featured image'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/images/aircraft/<int:aircraft_id>', methods=['GET'])
def get_aircraft_images(aircraft_id):
    """Get all images for a specific aircraft"""
    # Validate aircraft exists
    aircraft = Aircraft.query.get_or_404(aircraft_id)
    
    # Get query parameters
    approved_only = request.args.get('approved_only', default=True, type=lambda x: x.lower() == 'true')
    limit = request.args.get('limit', default=None, type=int)
    
    # Get images using service
    images = image_service.get_aircraft_images(
        aircraft_id=aircraft_id,
        approved_only=approved_only,
        limit=limit
    )
    
    return jsonify({
        'images': [image.to_dict() for image in images],
        'count': len(images)
    })


@bp.route('/images/featured/<int:aircraft_id>', methods=['GET'])
def get_featured_image(aircraft_id):
    """Get the featured image for an aircraft"""
    # Validate aircraft exists
    aircraft = Aircraft.query.get_or_404(aircraft_id)
    
    # Get featured image using service
    image = image_service.get_featured_image(aircraft_id)
    
    if image:
        return jsonify(image.to_dict())
    else:
        return jsonify({'message': 'No featured image found'}), 404


@bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    # Security: ensure filename is properly secured
    safe_filename = secure_filename(filename)
    
    # Construct the path safely
    base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'app/static/uploads')
    file_path = os.path.join(base_path, safe_filename)
    
    # Ensure the file_path is within the allowed directory
    if not file_path.startswith(base_path):
        return jsonify({'error': 'Invalid file path'}), 400
    
    directory = os.path.dirname(file_path)
    filename_only = os.path.basename(file_path)
    
    return send_from_directory(directory, filename_only)
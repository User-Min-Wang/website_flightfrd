import os
import uuid
from PIL import Image as PILImage
from datetime import datetime
from extensions import db
from app.models import Image, Aircraft, User
from app.utils.formatters import format_file_size


class ImageService:
    """
    Service class for handling aircraft image uploads, processing, and management
    """
    
    def __init__(self, upload_folder, allowed_extensions=None, max_size_mb=16):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions or {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
        self.max_size_mb = max_size_mb
        self.thumbnail_sizes = {
            'small': (200, 200),
            'medium': (500, 500),
            'large': (1000, 1000)
        }

    def save_image(self, file, aircraft_id, user_id=None, description=None, image_type='photo', license='copyright'):
        """
        Save an uploaded image with validation and processing
        
        Args:
            file: Uploaded file object
            aircraft_id: ID of associated aircraft
            user_id: ID of uploading user (optional)
            description: Description of the image
            image_type: Type of image (photo, diagram, etc.)
            license: License type
            
        Returns:
            Image: Created image object
        """
        try:
            # Validate aircraft exists
            aircraft = Aircraft.query.get(aircraft_id)
            if not aircraft:
                raise ValueError(f"Aircraft with ID {aircraft_id} not found")
            
            # Validate user exists if provided
            user = None
            if user_id:
                user = User.query.get(user_id)
                if not user:
                    raise ValueError(f"User with ID {user_id} not found")
            
            # Validate file extension
            _, ext = os.path.splitext(file.filename.lower())
            if ext not in self.allowed_extensions:
                raise ValueError(f"File extension {ext} not allowed. Allowed: {', '.join(self.allowed_extensions)}")
            
            # Check file size
            file.seek(0, os.SEEK_END)  # Go to end of file
            file_size = file.tell()  # Get current position (file size)
            file.seek(0)  # Reset file pointer to beginning
            
            max_size_bytes = self.max_size_mb * 1024 * 1024
            if file_size > max_size_bytes:
                raise ValueError(f"File size {format_file_size(file_size)} exceeds maximum {self.max_size_mb}MB")
            
            # Generate unique filename
            unique_filename = f"{uuid.uuid4().hex}{ext}"
            subfolder = self._get_subfolder_for_aircraft(aircraft_id)
            file_path = os.path.join(self.upload_folder, subfolder, unique_filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save original image
            pil_image = PILImage.open(file)
            pil_image.save(file_path)
            
            # Get image dimensions
            width, height = pil_image.size
            
            # Create thumbnail
            thumbnail_path = self._create_thumbnail(pil_image, subfolder, unique_filename)
            
            # Create image record in database
            image_record = Image(
                filename=file.filename,
                filepath=file_path,
                thumbnail_path=thumbnail_path,
                aircraft_id=aircraft_id,
                uploaded_by=user_id,
                description=description,
                image_type=image_type,
                size_bytes=file_size,
                width=width,
                height=height,
                license=license,
                copyright_holder=user.username if user else None,
                upload_date=datetime.utcnow()
            )
            
            db.session.add(image_record)
            db.session.commit()
            
            return image_record
            
        except Exception as e:
            db.session.rollback()
            raise e

    def _get_subfolder_for_aircraft(self, aircraft_id):
        """
        Determine subfolder based on aircraft ID for organized storage
        
        Args:
            aircraft_id: ID of aircraft
            
        Returns:
            str: Subfolder path
        """
        # Use last two digits of aircraft ID to create subfolders (00-99)
        subfolder_num = aircraft_id % 100
        return f"{subfolder_num:02d}"

    def _create_thumbnail(self, pil_image, subfolder, original_filename):
        """
        Create a thumbnail for the image
        
        Args:
            pil_image: PIL Image object
            subfolder: Subfolder for image storage
            original_filename: Original filename
            
        Returns:
            str: Path to thumbnail
        """
        try:
            # Create thumbnail path
            name, ext = os.path.splitext(original_filename)
            thumbnail_filename = f"{name}_thumb.jpg"  # Thumbnails always saved as JPG
            thumbnail_path = os.path.join(self.upload_folder, 'thumbnails', subfolder, thumbnail_filename)
            
            # Ensure thumbnail directory exists
            os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
            
            # Create thumbnail
            pil_image.thumbnail(self.thumbnail_sizes['medium'], PILImage.LANCZOS)
            pil_image.save(thumbnail_path, 'JPEG', quality=85, optimize=True)
            
            return thumbnail_path
            
        except Exception as e:
            # Log error but don't fail the entire operation
            print(f"Error creating thumbnail: {str(e)}")
            return None

    def get_aircraft_images(self, aircraft_id, approved_only=True, limit=None):
        """
        Retrieve images for a specific aircraft
        
        Args:
            aircraft_id: ID of aircraft
            approved_only: Whether to return only approved images
            limit: Maximum number of images to return
            
        Returns:
            list: List of image objects
        """
        try:
            query = Image.query.filter_by(aircraft_id=aircraft_id)
            
            if approved_only:
                query = query.filter_by(approved=True)
            
            query = query.order_by(Image.upload_date.desc())
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
            
        except Exception as e:
            raise e

    def get_featured_image(self, aircraft_id):
        """
        Get the featured image for an aircraft
        
        Args:
            aircraft_id: ID of aircraft
            
        Returns:
            Image: Featured image object or None
        """
        try:
            image = Image.query.filter_by(aircraft_id=aircraft_id, is_featured=True, approved=True)\
                              .order_by(Image.upload_date.desc()).first()
            
            # If no featured image, return the most recent approved image
            if not image:
                image = Image.query.filter_by(aircraft_id=aircraft_id, approved=True)\
                                  .order_by(Image.upload_date.desc()).first()
            
            return image
            
        except Exception as e:
            raise e

    def approve_image(self, image_id, approver_id):
        """
        Approve an image for public display
        
        Args:
            image_id: ID of image to approve
            approver_id: ID of user approving the image
            
        Returns:
            bool: Success status
        """
        try:
            image = Image.query.get(image_id)
            if not image:
                raise ValueError(f"Image with ID {image_id} not found")
            
            approver = User.query.get(approver_id)
            if not approver:
                raise ValueError(f"Approver with ID {approver_id} not found")
            
            image.approved = True
            image.approved_by = approver_id
            image.approved_date = datetime.utcnow()
            
            db.session.commit()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            raise e

    def set_featured_image(self, image_id, aircraft_id):
        """
        Set an image as the featured image for an aircraft
        
        Args:
            image_id: ID of image to feature
            aircraft_id: ID of aircraft
            
        Returns:
            bool: Success status
        """
        try:
            # Verify image belongs to aircraft
            image = Image.query.filter_by(id=image_id, aircraft_id=aircraft_id).first()
            if not image:
                raise ValueError(f"Image with ID {image_id} does not belong to aircraft {aircraft_id}")
            
            # Remove featured status from other images of this aircraft
            db.session.execute(
                Image.__table__.update()
                .where(Image.aircraft_id == aircraft_id)
                .values(is_featured=False)
            )
            
            # Set this image as featured
            image.is_featured = True
            db.session.commit()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_image(self, image_id, user_id=None):
        """
        Delete an image and its associated files
        
        Args:
            image_id: ID of image to delete
            user_id: ID of user requesting deletion (for permission check)
            
        Returns:
            bool: Success status
        """
        try:
            image = Image.query.get(image_id)
            if not image:
                raise ValueError(f"Image with ID {image_id} not found")
            
            # Check permissions - only admins, moderators, or image uploader can delete
            if user_id:
                user = User.query.get(user_id)
                if not user or (user.role not in ['admin', 'moderator'] and user.id != image.uploaded_by):
                    raise PermissionError("Insufficient permissions to delete this image")
            
            # Delete files
            if os.path.exists(image.filepath):
                os.remove(image.filepath)
            
            if image.thumbnail_path and os.path.exists(image.thumbnail_path):
                os.remove(image.thumbnail_path)
            
            # Delete database record
            db.session.delete(image)
            db.session.commit()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            raise e
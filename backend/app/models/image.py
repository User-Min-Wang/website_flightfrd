from extensions import db
from datetime import datetime


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)  # Original filename
    filepath = db.Column(db.String(500), nullable=False)  # Full path to image
    thumbnail_path = db.Column(db.String(500))  # Path to thumbnail version
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircraft.id'), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # User who uploaded
    description = db.Column(db.Text)  # Description of the image
    image_type = db.Column(db.String(50), default='photo')  # photo, diagram, etc.
    size_bytes = db.Column(db.Integer)  # File size in bytes
    width = db.Column(db.Integer)  # Image width in pixels
    height = db.Column(db.Integer)  # Image height in pixels
    is_featured = db.Column(db.Boolean, default=False)  # Featured image for aircraft
    license = db.Column(db.String(50), default='copyright')  # License type
    copyright_holder = db.Column(db.String(200))  # Copyright holder
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=False)  # Approval status
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # User who approved
    approved_date = db.Column(db.DateTime)  # Date of approval
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Image {self.filename}>'

    def to_dict(self):
        """Convert image object to dictionary representation"""
        return {
            'id': self.id,
            'filename': self.filename,
            'filepath': self.filepath,
            'thumbnail_path': self.thumbnail_path,
            'aircraft_id': self.aircraft_id,
            'uploaded_by': self.uploaded_by,
            'description': self.description,
            'image_type': self.image_type,
            'size_bytes': self.size_bytes,
            'width': self.width,
            'height': self.height,
            'is_featured': self.is_featured,
            'license': self.license,
            'copyright_holder': self.copyright_holder,
            'upload_date': self.upload_date.isoformat(),
            'approved': self.approved,
            'approved_by': self.approved_by,
            'approved_date': self.approved_date.isoformat() if self.approved_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
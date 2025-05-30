from datetime import datetime
from app.extensions import db

class Job(db.Model):
    id = db.Column(db.String, primary_key=True)   # uuid4 hex
    student_name = db.Column(db.String(100))
    student_email = db.Column(db.String(100))
    discipline = db.Column(db.String(50))
    class_number = db.Column(db.String(50))
    original_filename = db.Column(db.String(256))
    display_name = db.Column(db.String(256))  # Standardized name used in dashboard and filenames
    file_path = db.Column(db.String(512))         # Path to authoritative file
    metadata_path = db.Column(db.String(512))     # Path to metadata.json
    status = db.Column(db.String(50))
    printer = db.Column(db.String(64))
    color = db.Column(db.String(32))
    material = db.Column(db.String(32))
    weight_g = db.Column(db.Float)
    time_hours = db.Column(db.Float)
    cost_usd = db.Column(db.Numeric(6, 2))
    acknowledged_minimum_charge = db.Column(db.Boolean, default=False)
    student_confirmed = db.Column(db.Boolean, default=False)
    student_confirmed_at = db.Column(db.DateTime, nullable=True)
    confirm_token = db.Column(db.String(128), nullable=True, unique=True)
    confirm_token_expires = db.Column(db.DateTime, nullable=True)
    reject_reasons = db.Column(db.JSON, nullable=True)
    staff_viewed_at = db.Column(db.DateTime, nullable=True)  # For tracking unreviewed jobs and visual alerts
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_updated_by = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)  # Staff/internal notes for this job
    events = db.relationship('Event', backref='job', lazy=True) # Relationship to Event 
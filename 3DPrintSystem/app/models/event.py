from datetime import datetime
from app.extensions import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String, db.ForeignKey('job.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    event_type = db.Column(db.String(50)) # e.g., 'JobCreated', 'StaffApproved', 'EmailSent'
    details = db.Column(db.JSON, nullable=True) # Contextual info
    triggered_by = db.Column(db.String(50)) # 'student', 'staff', 'system' 
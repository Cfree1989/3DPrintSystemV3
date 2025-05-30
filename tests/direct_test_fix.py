import os
import sys
import uuid
from datetime import datetime

# Add parent directory to path so we can import the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    # Set required environment variables
    os.environ['SECRET_KEY'] = 'testkey12345'
    os.environ['DATABASE_URL'] = 'sqlite:///instance/3dprint.db'
    os.environ['STAFF_PASSWORD'] = 'Fabrication'
    os.environ['STORAGE_PATH'] = 'storage'
    
    # Import the required modules from our app
    from 3DPrintSystem.app.services.file_service import save_uploaded_file
    from 3DPrintSystem.app import create_app
    from 3DPrintSystem.app.extensions import db
    from 3DPrintSystem.app.models.job import Job
    from 3DPrintSystem.app.models.event import Event

    print("Successfully imported all modules")
    
    # Initialize the Flask app
    app = create_app()
    app.config['TESTING'] = True
    
    # Create a Flask test context
    with app.app_context():
        try:
            # Test data (equivalent to form data)
            form_data = {
                'studentName': 'Test User',
                'studentEmail': 'test@example.com',
                'discipline': 'Engineering',
                'classNumber': 'TEST 1000',
                'printMethod': 'Filament',
                'colorPreference': 'True Red',
                'printer': 'Prusa MK4S',
                'minChargeConsent': 'yes'
            }
            
            # Create a mock file object
            class MockFile:
                def __init__(self, filename, content=b'test content'):
                    self.filename = filename
                    self.content = content
                    
                def save(self, path):
                    with open(path, 'wb') as f:
                        f.write(self.content)
            
            # Use a test file
            test_file = MockFile('test_model.stl')
            
            print("Step 1: Testing file upload...")
            display_name, file_path, metadata_path = save_uploaded_file(test_file, form_data)
            
            if display_name and file_path and metadata_path:
                print(f"✓ File upload successful")
                print(f"  - Display name: {display_name}")
                print(f"  - File path: {file_path}")
                print(f"  - Metadata path: {metadata_path}")
            else:
                print("✗ File upload failed")
                sys.exit(1)
            
            print("\nStep 2: Testing database operations...")
            # Create database job record
            job_id = str(uuid.uuid4())
            
            job = Job(
                id=job_id,
                student_name=form_data['studentName'],
                student_email=form_data['studentEmail'],
                discipline=form_data['discipline'],
                class_number=form_data['classNumber'],
                original_filename=test_file.filename,
                display_name=display_name,
                file_path=file_path,
                metadata_path=metadata_path,
                status='UPLOADED',
                printer=form_data['printer'],
                color=form_data['colorPreference'],
                material=form_data['printMethod'],
                acknowledged_minimum_charge=True,
                student_confirmed=False,
                last_updated_by='student',
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Create JobCreated event
            event = Event(
                job_id=job_id,
                event_type='JobCreated',
                triggered_by='student',
                details={
                    'student_name': form_data['studentName'],
                    'student_email': form_data['studentEmail'],
                    'original_filename': test_file.filename,
                    'display_name': display_name,
                    'print_method': form_data['printMethod'],
                    'color': form_data['colorPreference'],
                    'printer': form_data['printer']
                },
                timestamp=datetime.utcnow()
            )
            
            # Save to database
            db.session.add(job)
            db.session.add(event)
            db.session.commit()
            
            print(f"✓ Database operations successful")
            print(f"  - Job ID: {job_id}")
            print(f"  - Event ID: {event.id}")
            
            print("\nAll tests passed successfully!")
            
        except Exception as e:
            print(f"Error during test: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
except ImportError as e:
    print(f"Import error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 
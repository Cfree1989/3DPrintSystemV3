import os
import sys
import psycopg2
from urllib.parse import urlparse

# Get database URL from environment or use default
db_url = os.environ.get('DATABASE_URL', 'postgres://fablab_user:fablab@localhost:5432/3d_print_system')
print(f"Testing connection to: {db_url}")

try:
    # Parse the database URL
    parsed = urlparse(db_url)
    username = parsed.username
    password = parsed.password
    database = parsed.path[1:]
    hostname = parsed.hostname
    port = parsed.port or 5432
    
    # Connect to the database
    conn = psycopg2.connect(
        host=hostname,
        database=database,
        user=username,
        password=password,
        port=port
    )
    
    # Create a cursor
    cursor = conn.cursor()
    
    # Execute a query to get all jobs
    cursor.execute("SELECT id, student_name, student_email, status, created_at FROM job ORDER BY created_at DESC")
    rows = cursor.fetchall()
    
    if rows:
        print(f"Found {len(rows)} jobs:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Status: {row[3]}, Created: {row[4]}")
        
        # Get events for the most recent job
        latest_job_id = rows[0][0]
        cursor.execute("SELECT id, event_type, triggered_by, timestamp FROM event WHERE job_id = %s ORDER BY timestamp DESC", (latest_job_id,))
        events = cursor.fetchall()
        
        if events:
            print(f"\nEvents for job {latest_job_id}:")
            for event in events:
                print(f"Event ID: {event[0]}, Type: {event[1]}, Triggered by: {event[2]}, Time: {event[3]}")
        else:
            print(f"\nNo events found for job {latest_job_id}")
    else:
        print("No jobs found in the database.")
    
    # Close the connection
    cursor.close()
    conn.close()
    sys.exit(0)
    
except Exception as e:
    print(f"Error connecting to database: {e}")
    sys.exit(1) 
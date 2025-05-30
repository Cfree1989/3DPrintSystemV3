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
    
    # Execute a simple query
    cursor.execute("SELECT count(*) FROM job")
    count = cursor.fetchone()[0]
    print(f"Success! Found {count} jobs in the database.")
    
    # Check for events too
    cursor.execute("SELECT count(*) FROM event")
    event_count = cursor.fetchone()[0]
    print(f"Found {event_count} events in the database.")
    
    # Close the connection
    cursor.close()
    conn.close()
    sys.exit(0)
    
except Exception as e:
    print(f"Error connecting to database: {e}")
    sys.exit(1) 
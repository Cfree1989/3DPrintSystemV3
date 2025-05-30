import requests
import os
import sys

# Define the form data
form_data = {
    'student_name': 'Test User',
    'student_email': 'test@example.com',
    'discipline': 'Engineering',
    'class_number': 'TEST 1000',
    'print_method': 'Filament',
    'color': 'True Red',
    'printer': 'Prusa MK4S',
    'acknowledged_minimum_charge': 'yes'
}

# URL to submit to
url = 'http://localhost:5000/submit'

# The file to upload
file_path = 'test_cube.stl'

try:
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        sys.exit(1)
    
    # Prepare the file for upload
    files = {
        'file': (os.path.basename(file_path), open(file_path, 'rb'), 'application/sla')
    }
    
    # Make the POST request
    print(f"Submitting form to {url}...")
    response = requests.post(url, data=form_data, files=files)
    
    # Check the response
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        print("Form submitted successfully!")
        if "success" in response.url:
            print(f"Redirected to success page: {response.url}")
        else:
            print("Warning: No redirect to success page detected.")
            print(f"Current page: {response.url}")
    else:
        print(f"Form submission failed with status code {response.status_code}")
        print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
    
except Exception as e:
    print(f"Error during form submission: {e}")
    sys.exit(1)
finally:
    # Close the file
    if 'files' in locals() and 'file' in files:
        files['file'][1].close() 
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration from environment variables
mail_server = os.environ.get('MAIL_SERVER', 'smtp.office365.com')
mail_port = int(os.environ.get('MAIL_PORT', 587))
mail_use_tls = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
mail_username = os.environ.get('MAIL_USERNAME', 'coad-fablab@lsu.edu')
mail_password = os.environ.get('MAIL_PASSWORD', '')
mail_default_sender = os.environ.get('MAIL_DEFAULT_SENDER', 'coad-fablab@lsu.edu')

# Test parameters
recipient = mail_username  # Send test email to ourselves
subject = "3D Print System Test Email"
body = """
This is a test email from the 3D Print System.
If you're receiving this, the email configuration is working correctly.

Server: {server}
Port: {port}
TLS: {tls}
Username: {username}
""".format(
    server=mail_server, 
    port=mail_port, 
    tls=mail_use_tls,
    username=mail_username
)

print(f"Testing email configuration:")
print(f"Server: {mail_server}")
print(f"Port: {mail_port}")
print(f"TLS: {mail_use_tls}")
print(f"Username: {mail_username}")
print(f"Password: {'*' * len(mail_password) if mail_password else 'Not set'}")
print(f"Default Sender: {mail_default_sender}")
print(f"Recipient: {recipient}")

if not mail_password:
    print("\nError: MAIL_PASSWORD environment variable is not set.")
    print("Cannot proceed with email test. Set the password and try again.")
    sys.exit(1)

try:
    # Create message
    msg = MIMEMultipart()
    msg['From'] = mail_default_sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    # Connect to the server
    print("\nAttempting to connect to the mail server...")
    server = smtplib.SMTP(mail_server, mail_port)
    server.ehlo()
    
    # Use TLS if configured
    if mail_use_tls:
        print("Starting TLS...")
        server.starttls()
        server.ehlo()
    
    # Login
    print(f"Logging in as {mail_username}...")
    server.login(mail_username, mail_password)
    
    # Send email
    print("Sending test email...")
    server.send_message(msg)
    
    # Close connection
    server.quit()
    
    print("\nTest email sent successfully!")
    print(f"Check {recipient} for the test email.")
    sys.exit(0)
    
except Exception as e:
    print(f"\nError sending test email: {e}")
    sys.exit(1) 
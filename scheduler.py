import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email account credentials (use a separate email for this!)
EMAIL_ADDRESS = 'your_email@example.com'
EMAIL_PASSWORD = 'your_password'

def schedule_interview(candidate):
    """Send an interview invitation email to the shortlisted candidate."""
    recipient_email = candidate.get('email')

    # Skip if email is unknown
    if not recipient_email or recipient_email == "Unknown":
        print(f"Skipping email for {candidate.get('name')}, email unknown.")
        return

    # Email content
    subject = "Interview Invitation"
    body = f"""\
Hi {candidate.get('name', 'Candidate')},

Congratulations! Based on your profile, you have been shortlisted for an interview.

Please reply to this email to schedule a suitable time.

Best regards,  
HR Team
"""

    # Set up the MIME email
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Send the email
        server.send_message(msg)
        server.quit()

        print(f"Interview invitation sent to {recipient_email} ✅")

    except Exception as e:
        print(f"Failed to send email to {recipient_email}. ❌ Error: {e}")

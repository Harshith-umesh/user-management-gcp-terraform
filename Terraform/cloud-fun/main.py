import os
import requests
from google.cloud import pubsub_v1
import base64
import json
from datetime import datetime, timedelta
import secrets
import urllib.parse

def send_verification_email(event, context):
    """Triggered by a Pub/Sub message. Sends a verification email."""
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    message_data = json.loads(pubsub_message)
    
    user_email = message_data['email']
    verification_link = generate_verification_link(user_email)

    mailgun_domain = os.environ.get('MAILGUN_DOMAIN')
    mailgun_api_key = os.environ.get('MAILGUN_API_KEY')

    response = requests.post(
        f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
        auth=("api", mailgun_api_key),
        data={
            "from": f"Bharath Bhaskar <mailgun@{mailgun_domain}>",
            "to": [user_email],
            "subject": "Verify your email address",
            "text": f"Please click on the link to verify your email: {verification_link}"
        }
    )

    print(f"Email sent to {user_email}: {response.text}")



def generate_verification_link(email):
    """
    Generates a secure verification link with a unique token and expiration time.
    
    Args:
    email (str): The user's email address to verify.
    
    Returns:
    str: A verification link with a unique token and expiration time.
    """

    verification_token = secrets.token_urlsafe()
    
    expiration_time = datetime.utcnow() + timedelta(minutes=2)
    
    # Ensure the email and expiration time are URL-encoded to be safely included in the query parameters
    encoded_email = urllib.parse.quote(email)
    encoded_expiration = urllib.parse.quote(expiration_time.isoformat())

    link = f"http://harshithcloud.me:8080/verify?token={verification_token}&email={encoded_email}&expires={encoded_expiration}"
    
    return link


def simulate_pubsub_message(email):
    message_dict = {"email": email}
    message_json = json.dumps(message_dict)
    message_bytes = message_json.encode("utf-8")
    base64_bytes = base64.b64encode(message_bytes)
    return {"data": base64_bytes}

# Example usage of the simulated event
if __name__ == "__main__":
    email = "harshith.umesh.nat@gmail.com"
    verification_link = generate_verification_link(email)
    print(verification_link)
    simulated_event = simulate_pubsub_message(email)
    context = {}  # Context can be empty if not used in the function
    send_verification_email(simulated_event, context)





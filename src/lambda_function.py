import boto3
import csv
import json
import random
import requests
from botocore.exceptions import NoCredentialsError

# Initialize S3 and SES clients
s3_client = boto3.client('s3')
ses_client = boto3.client('ses')

# S3 bucket and file name
BUCKET_NAME = 'goal-manifest-2025'
FILE_NAME = 'goals.csv'

# SES sender and recipient
SENDER_EMAIL = 'your-email@example.com'

def fetch_quote():
    """Fetch a random motivational quote from ZenQuotes API."""
    try:
        response = requests.get("https://zenquotes.io/api/random")
        if response.status_code == 200:
            quote = response.json()[0]['q']  # Extract the quote
            author = response.json()[0]['a']  # Extract the author
            return f'"{quote}" - {author}'
        else:
            return "Stay motivated! Keep pushing forward!"
    except Exception as e:
        print(f"Error fetching quote: {e}")
        return "Stay motivated! Keep pushing forward!"

def get_random_goal():
    """Fetch a random goal from the CSV file in S3."""
    try:
        # Download the CSV file from S3
        s3_client.download_file(BUCKET_NAME, FILE_NAME, '/tmp/goals.csv')
        
        # Read the CSV file and pick a random goal
        with open('/tmp/goals.csv', 'r') as file:
            goals = list(csv.reader(file))
            return random.choice(goals)[0]  # Assuming each row has one goal
    except Exception as e:
        print(f"Error fetching goal: {e}")
        return "Achieve greatness!"

def send_email(recipient_email, subject, body):
    """Send an email using Amazon SES."""
    try:
        response = ses_client.send_email(
            Source=SENDER_EMAIL,
            Destination={'ToAddresses': [recipient_email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        print(f"Email sent! Message ID: {response['MessageId']}")
    except NoCredentialsError:
        print("AWS credentials not found.")
    except Exception as e:
        print(f"Error sending email: {e}")

def lambda_handler(event, context):
    """Main Lambda function handler."""
    recipient_email = event.get('recipient_email')  # Get the recipient email from event
    if not recipient_email:
        return {"statusCode": 400, "body": "Recipient email not provided."}
    
    # Get a random goal and quote
    random_goal = get_random_goal()
    motivational_quote = fetch_quote()
    
    # Email subject and body
    subject = "Your 2025 Goal & Motivation for Today!"
    body = f"Goal: {random_goal}\nMotivation: {motivational_quote}"
    
    # Send email
    send_email(recipient_email, subject, body)
    return {"statusCode": 200, "body": "Email sent successfully!"}

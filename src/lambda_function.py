import boto3
import csv
import random
import json
import urllib.request

# Initialize SNS client
sns_client = boto3.client('sns')

# SNS Topic ARN (Update with your SNS Topic ARN)
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:871740193993:GoalNotification'
S3_BUCKET_NAME = 'goal-manifestation-goals'
S3_FILE_KEY = 'goals.csv'


def fetch_quote():
    """Fetch a random motivational quote from ZenQuotes API."""
    try:
        response = urllib.request.urlopen("https://zenquotes.io/api/random")
        status_code = response.getcode()  # Use getcode() to get the status code
        if status_code == 200:
            data = response.read().decode()  # Decode the response content
            quote_data = json.loads(data)[0]  # Parse JSON and extract the first quote
            quote = quote_data['q']  # Extract the quote
            author = quote_data['a']  # Extract the author
            return f'"{quote}" - {author}'
        else:
            return "Stay motivated! Keep pushing forward!"
    except Exception as e:
        print(f"Error fetching quote: {e}")
        return "Stay motivated! Keep pushing forward!"

def get_random_goal():
    """Fetch a random goal from the CSV file stored in S3."""
    try:
        # Fetch the CSV file from S3
        s3_object = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=S3_FILE_KEY)
        csv_data = s3_object['Body'].read().decode('utf-8').splitlines()
        goals = list(csv.reader(csv_data))

        # Flatten the list of goals and pick a random one
        goal_list = [goal[0] for goal in goals]
        return random.choice(goal_list)
    except Exception as e:
        print(f"Error fetching goal: {e}")
        return "Achieve greatness!"

def send_sns_notification(recipient_email, subject, body):
    """Send an email using SNS to any random email address."""
    try:
        # Publish the message to the SNS topic
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=body,
            Subject=subject,
            MessageAttributes={
                'email': {
                    'DataType': 'String',
                    'StringValue': recipient_email
                }
            }
        )
        print(f"Message sent! Message ID: {response['MessageId']}")
        return {
            'status': 'success',
            'message': 'Email sent successfully via SNS'
        }
    except Exception as e:
        print(f"Error sending SNS notification: {e}")
        return {
            'status': 'error',
            'message': str(e)
        }

def lambda_handler(event, context):
    """Main Lambda function handler."""
    try:
        # Parse the email from the request body
        body = json.loads(event['body'])
        recipient_email = body.get('recipient_email', 'No email provided')

        # Fetch goal and quote
        goal = get_random_goal()
        quote = fetch_quote()

        # Prepare email body
        email_body = f"Your Goal for Today: {goal}\n\nMotivational Quote: {quote}"

        # Send the email using SNS
        result = send_sns_notification(recipient_email, "Goal and Motivation for the Day", email_body)

        # Prepare the response
        response_body = {
            "message": f"Goal and motivation email sent to {recipient_email}!"
        }

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": json.dumps(response_body),
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error."})
        }

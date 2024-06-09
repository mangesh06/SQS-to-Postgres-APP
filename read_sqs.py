import boto3
import psycopg2
import json
import hashlib
from botocore.config import Config

# Set up localstack configuration
localstack_config = Config(
    region_name='us-east-1',
    signature_version='v4',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

# Initialize SQS client with localstack configuration
sqs = boto3.client('sqs', config=localstack_config, endpoint_url='http://localhost:4566', aws_access_key_id='dummy', aws_secret_access_key='dummy')

# Queue URL
queue_url = 'http://localhost:4566/000000000000/login-queue'
print(f'Queue URL: {queue_url}')

def read_messages_from_sqs():
    try:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10
        )
        print(f'Response from SQS: {response}')

        messages = response.get('Messages', [])
        if not messages:
            print("No messages found in the queue.")
            return []

        for message in messages:
            print(f"Message Body: {message['Body']}")
            try:
                data = process_message(message['Body'])
                print(f"Processed Data: {data}")
                write_to_postgres(data)
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
            # Delete the message from the queue after processing
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
    except Exception as e:
        print(f"Error reading messages from SQS: {e}")

def process_message(message_body):
    try:
        data = json.loads(message_body)
        salt = "fetch_rewards"
        data['masked_device_id'] = hashlib.sha256((data['device_id'] + salt).encode()).hexdigest()
        data['masked_ip'] = hashlib.sha256((data['ip'] + salt).encode()).hexdigest()
        return data
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
        raise

def write_to_postgres(data):
    try:
        print("Connecting to the database...")
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost', port='5432')
        print("Connection established.")
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        print(f"Executing query with data: {data}")
        cursor.execute(insert_query, (data['user_id'], data['device_type'], data['masked_ip'], data['masked_device_id'], data['locale'], data['app_version'], data['create_date']))
        conn.commit()
        print("Data inserted successfully.")
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error inserting data: {e}")

if __name__ == "__main__":
    read_messages_from_sqs()

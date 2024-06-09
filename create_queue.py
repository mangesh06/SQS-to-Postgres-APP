import boto3
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

def create_queue():
    response = sqs.create_queue(QueueName='login-queue')
    print(f"Queue created. URL: {response['QueueUrl']}")

if __name__ == "__main__":
    create_queue()

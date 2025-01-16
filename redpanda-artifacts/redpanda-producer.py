import boto3
import csv
import time
from confluent_kafka import Producer
import json
import uuid

minio_host = "localhost:9000"  
access_key = "minio_user"      # Access key (credentials in the docker-compose-minio.yaml)
secret_key = "minio_password"  # Secret key (credentials in the docker-compose-minio.yaml)
bucket_name = "bucket"         # Defined in the docker compose
object_name = "data.csv"

# Initialize the S3 client
s3 = boto3.client(
    's3',
    endpoint_url=f'http://{minio_host}', # localhost as we run this on node-1 - to be decided 
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
)

# Redpanda configuration
BROKER_URL = 'localhost:9092' # TA notes - this is localhost as we run this on node-1. (TO be decided)
TOPIC_NAME = 'flight-info'    # created on the command link with the rpk command 

# Set up Redpanda producer
producer_config = {'bootstrap.servers': BROKER_URL}
producer = Producer(producer_config)

def produce_events():
    # Fetch dataset from MinIO
    print(f"Fetching dataset from MinIO bucket '{bucket_name}', object '{object_name}'...")
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_name)
    except Exception as e:
        print(f"Error fetching file from MinIO: {e}")
        return
    
    # Read from s3 store
    lines = response['Body'].read().decode('utf-8').splitlines()
    reader = csv.DictReader(lines)

    row_counter = 0 

    for row in reader:
        row_counter += 1
        event = json.dumps(row) 
        key = str(uuid.uuid4()) 
        
        # Produce to Redpanda
        try:
            producer.produce(TOPIC_NAME, key=key, value=event)
            producer.flush()  # Ensure the message is sent
            print(f"Processed line {row_counter}: {event}")  # Print the processed row info
        except Exception as e:
            print(f"Error producing event for row {row_counter}: {e}")

        time.sleep(0.5)  # Simulate real-time streaming

    print(f"Total rows processed: {row_counter}")

if __name__ == "__main__":
    print("Producer script starting...")
    produce_events()
    print("Producer script finished.")


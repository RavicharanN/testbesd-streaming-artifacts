import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os

# MinIO (or S3) connection details
minio_host = "192.168.1.11:9000"  
access_key = "minio_user"      # Access key (credentials in the docker-compose-minio.yaml)
secret_key = "minio_password"  # Secret key (credentials in the docker-compose-minio.yaml)
bucket_name = "bucket"         # Defined in the docker compose

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    endpoint_url=f'http://{minio_host}', 
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name='us-east-1',
)

try:
    s3_client.head_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' exists.")
except Exception as e:
    print(f"Bucket '{bucket_name}' does not exist. Creating it now...")
    s3_client.create_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' created.")

file_path = "data.csv" 
object_name = "data.csv" 

# TA notes - block can be removed 
if not os.path.isfile(file_path):
    print(f"File '{file_path}' does not exist!")
    exit(1)

try:
    s3_client.upload_file(file_path, bucket_name, object_name)
    print(f"File '{file_path}' uploaded successfully to '{bucket_name}/{object_name}'.")
except (NoCredentialsError, PartialCredentialsError):
    print("Invalid credentials. Please check your access key and secret key.")
except Exception as e:
    print(f"Error uploading file: {e}")


import boto3
from botocore.exceptions import NoCredentialsError
import requests

def generate_download_url(bucket_name, object_name, key, secret, expiration=10):
    """Generate a presigned URL for the S3 object."""
    s3_client = boto3.client(
        's3',
        aws_access_key_id=key,
        aws_secret_access_key=secret,
    )
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name,
                                                            'ResponseContentDisposition': 'attachment'},
                                                    ExpiresIn=expiration)
    except NoCredentialsError:
        print("Credentials not available")
        return None
    return response



def generate_upload_url(bucket_name, object_name, key, secret, content_type='image/png', expiration=10):
    """Generate a presigned URL to upload a file."""
    s3_client = boto3.client(
        's3',
        aws_access_key_id=key,
        aws_secret_access_key=secret,
    )
    try:
        response = s3_client.generate_presigned_url('put_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name,
                                                            'ContentType': content_type},
                                                    ExpiresIn=expiration)
    except Exception as e:
        print(e)
        return None
    return response


upload_file_name = 'Hero.png'
download_file_name = 'RTG.mp4'

# upload_url = generate_upload_url(constants.bucket_name, upload_file_name)
# print("Upload URL:", upload_url)

# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=constants.access_key,
#     aws_secret_access_key=constants.secret_access_key,
# )

# response = s3_client.generate_presigned_post(
#     Bucket=constants.bucket_name,
#     Key=upload_file_name,
#     ExpiresIn=10
# )

# print(response['url'])

# files = {'file': open(upload_file_name, 'rb')}
# r = requests.post(response['url'], data=response['fields'], files=files)
# print(r.status_code)

# url = generate_download_url(constants.bucket_name, download_file_name, expiration=10)
# print(url)

# response = requests.get(url)

# if response.status_code == 200:
#     with open(f'downloaded_{download_file_name}', 'wb') as file:
#         file.write(response.content)
# else:
#     print("Failed to download the file")

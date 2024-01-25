from flask import Flask, render_template, request, redirect, url_for
import os
import boto3
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv
from s3_utils import generate_download_url, generate_upload_url
import requests

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

app = Flask(__name__, template_folder='../frontend')

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

@app.route('/')
def index():
    bucket_contents = s3_client.list_objects(Bucket=S3_BUCKET_NAME)['Contents']
    return render_template('index.html', files=bucket_contents)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        upload_url = generate_upload_url(S3_BUCKET_NAME, file.filename, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, file.content_type)
        files = {'file': file}
        response = requests.put(upload_url, data=file.read())
        return redirect(url_for('index'))

@app.route('/download')
def download():
    try:
        bucket_contents = s3_client.list_objects(Bucket=S3_BUCKET_NAME).get('Contents', [])
        files_info = []

        for file in bucket_contents:
            file_info = {
                'key': file['Key'],
                'size': round(file['Size'] / 1024, 2),  # Size in KB
                'type': 'Video' if file['Key'].endswith(('.mp4', '.avi', '.mov')) else 'Image'  # Simplified type check
            }
            files_info.append(file_info)
    except KeyError:
        files_info = []
        print("Could not retrieve files from S3.")

    return render_template('download.html', files=files_info)


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import boto3
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv
import s3_utils
from s3_utils import generate_download_url, generate_upload_url
import requests

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

app = Flask(__name__, template_folder='../frontend', static_folder='frontend/static')
app.secret_key = os.getenv('FLASK_SECRET_KEY')


s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Handle file upload
        video = request.files['video']  # Changed from 'file' to 'video' to match the HTML form
        if video and video.filename != '':
            upload_url = generate_upload_url(S3_BUCKET_NAME, video.filename, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, video.content_type)
            files = {'file': video}
            response = requests.put(upload_url, data=video.read(), headers={'Content-Type': video.content_type})
            if response.status_code == 200:
                # Successful upload
                flash('Video uploaded successfully!')
            else:
                # Handle unsuccessful upload
                flash('Upload failed.')
            return redirect(url_for('index'))
    return render_template('upload.html')


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

@app.route('/download/<filename>')
def download_file(filename):
    download_url = generate_download_url(S3_BUCKET_NAME, filename, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    return redirect(download_url)


if __name__ == '__main__':
    app.run(debug=True)
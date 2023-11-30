import os
from flask import Flask, request, jsonify, send_file
from google.cloud import storage
import mimetypes
from io import BytesIO

app = Flask(__name__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\Flask\ltka-jalan-9f4fd8c00bb7.json" #Perlu diubah pathnya ....

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
   
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        # Initialize Google Cloud Storage client
        client = storage.Client()

        # Get the bucket
        bucket_name = 'awan-jalan-bucket'  # Replace with your bucket name
        bucket = client.bucket(bucket_name)
        
        # Get file extension and infer content type
        file_extension = file.filename.rsplit('.', 1)[-1].lower()
        content_type = mimetypes.guess_type(file.filename)[0]

        # Upload the file to the bucket
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file, content_type=content_type)

        # Make the uploaded file public
        blob.make_public()

        return jsonify({'message': 'File uploaded and made public successfully'})

@app.route('/download/<file_name>', methods=['GET'])
def download_file(file_name):
    # Initialize Google Cloud Storage client
    client = storage.Client()

    # Get the bucket
    bucket_name = 'awan-jalan-bucket'  # Replace with your bucket name
    bucket = client.bucket(bucket_name)

    # Specify the blob (file) to download
    blob = bucket.blob(file_name)

    # Download the file to a BytesIO object (in-memory file-like object)
    file_contents = BytesIO()
    blob.download_to_file(file_contents)
    file_contents.seek(0)  # Reset the pointer to the beginning of the stream

    # Use Flask's send_file to stream the file for download
    return send_file(file_contents, as_attachment=True, download_name=file_name)


if __name__ == '__main__':
    app.run(debug=True)
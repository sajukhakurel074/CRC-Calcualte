from flask import Flask, request, jsonify, send_from_directory
import binascii
import os

from flask_cors import CORS
CORS(app)

app = Flask(__name__, static_url_path='', static_folder='.')

def calculate_crc(data):
    return binascii.crc32(data) & 0xffffffff

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        data = file.read()
        crc_value = calculate_crc(data)
        return jsonify({'crc': crc_value})
    return jsonify({'error': 'File processing error'})

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)

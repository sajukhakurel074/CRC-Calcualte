from flask import Flask, request, jsonify, send_from_directory
import binascii
import os

# from flask_cors import CORS
# CORS(app)

app = Flask(__name__, static_url_path='', static_folder='.')

def calculate_crc(data):
    return binascii.crc32(data) & 0xffffffff

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return jsonify({'error': 'No files part'})
    
    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': 'No selected files'})

    crc_values = {}
    for file in files:
        if file.filename == '':
            continue
        data = file.read()
        crc_value = calculate_crc(data)
        crc_values[file.filename] = {
            'decimal': crc_value,
            'hex': hex(crc_value)
        }

    return jsonify({'crc_values': crc_values})

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)

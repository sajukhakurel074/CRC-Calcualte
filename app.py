from flask import Flask, request, jsonify, send_from_directory
import binascii
import os

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

    file_details = {}
    for file in files:
        if file.filename == '':
            continue
        data = file.read()
        crc_value = calculate_crc(data)
        file_details[file.filename] = {
            'size': len(data),
            'decimal_crc': crc_value,
            'hex_crc': hex(crc_value)
        }

    return jsonify({'file_details': file_details})

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)

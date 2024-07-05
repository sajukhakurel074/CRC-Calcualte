import binascii
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        data = file.read()
        crc_value = binascii.crc32(data) & 0xffffffff
        return jsonify({'crc': crc_value})
    return jsonify({'error': 'File processing error'})

if __name__ == "__main__":
    app.run()

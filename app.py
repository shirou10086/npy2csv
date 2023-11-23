from flask import Flask, request, jsonify, send_file
import numpy as np
import csv
import os

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    npy_data = np.load(file)
    csv_filename = file.filename.replace('.npy', '.csv')
    csv_filepath = os.path.join('uploads', csv_filename)
    os.makedirs('uploads', exist_ok=True)
    with open(csv_filepath, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(npy_data)
    download_link = '/download/' + csv_filename
    return jsonify({'download_link': download_link})

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    csv_filepath = os.path.join('uploads', filename)
    return send_file(csv_filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

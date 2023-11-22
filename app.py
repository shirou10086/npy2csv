import numpy as np
import csv
import os
from flask import Flask, request, send_file, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        npy_data = np.load(file)
        csv_filename = file.filename.replace('.npy', '.csv')
        csv_filepath = os.path.join('uploads', csv_filename)
        os.makedirs('uploads', exist_ok=True)
        with open(csv_filepath, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(npy_data)
        return f'''
        CSV file "{csv_filename}" created successfully! 
        <a href="/download/{csv_filename}">Download CSV</a>
        '''
    return '''
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    '''

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    csv_filepath = os.path.join('uploads', filename)
    return send_file(csv_filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

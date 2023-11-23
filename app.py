from flask import Flask, request, send_file, render_template_string, after_this_request, url_for

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

        download_url = url_for('download', filename=csv_filename)
        return render_template_string('''
            <script type="text/javascript">
                window.onload = function() {
                    window.location.href = "{{ download_url }}";
                    setTimeout(function() {
                        window.location.href = "{{ index_url }}";
                    }, 3000); // 5秒后重定向回主页
                };
            </script>
        ''', download_url=download_url, index_url=url_for('index'))

    return '''
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    '''

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    csv_filepath = os.path.join('uploads', filename)

    @after_this_request
    def remove_file(response):
        try:
            os.remove(csv_filepath)
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    return send_file(csv_filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

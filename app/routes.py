from flask import current_app as app, flash, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import dataaccess.musical_work
import json

@app.route('/api/musical_work/iswc/<string:iswc>', methods=['GET'])
def retrieve_musical_work(iswc):
    musical_work = dataaccess.musical_work.get_musical_work(iswc)
    print(json.dumps(musical_work, indent=2), flush=True)
    return 'You sent ' + iswc


# @api.route("/files/<path:path>")
# def get_file(path):
#     """Download a file."""
#     return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


# @api.route("/files/<filename>", methods=["POST"])
# def post_file(filename):
#     """Upload a file."""

#     if "/" in filename:
#         # Return 400 BAD REQUEST
#         abort(400, "no subdirectories directories allowed")

#     with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
#         fp.write(request.data)

#     # Return 201 CREATED
#     return "", 201

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/api/musical_work', methods=['GET', 'POST'])
def upload_file():
    # if request.method == 'GET':

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
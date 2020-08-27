from flask import current_app as app, flash, request, redirect, url_for, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
import dataaccess.musical_work
import util.csv
import re

# get a musical work given its iswc; 
# @returns: json object
@app.route('/api/musical_work/<string:iswc>', methods=['GET'])
def get_musical_work(iswc):
    musical_work = dataaccess.musical_work.get_by_iswc(iswc)
    return jsonify(results=musical_work)

# get all musical works; 
# @returns: json object
@app.route('/api/musical_work', methods=['GET'])
def get_all_musical_works():
    musical_works = dataaccess.musical_work.get_all()
    return jsonify(results=musical_works)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# get the musical work given its iswc, in a csv format
# @returns: csv file or null
@app.route('/api/musical_work/<string:iswc>/download', methods=['GET'])
def download_single_musical_work(iswc):
    musical_work = dataaccess.musical_work.get_by_iswc(iswc)
    #TODO: check length
    musical_work = musical_work[0]
    ##### reformat result
    musical_work = dict(musical_work)
    contributors = str(musical_work['contributors']).replace('[','').replace(']','').replace(', ', '|')
    contributors = re.sub(r'\'', '', contributors) 
    musical_work['contributors'] = contributors
    ############
    util.csv.write_dict_as_csv(name='work_metadata', _dict=musical_work, dest=app.config['DOWNLOAD_FOLDER'])
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], 'work_metadata.csv', as_attachment=True)

# get all musical works in a csv format
# @returns: csv file
# @app.route('/api/musical_work/download', methods=['GET'])
# def download_all_musical_workds(iswc):
#     musical_work = dataaccess.musical_work.get_by_iswc(iswc)
#     musical_work = musical_work[0]
#     # reformat result
#     musical_work = dict(musical_work)
#     contributors = str(musical_work['contributors']).replace('[','').replace(']','').replace(', ', '|')
#     contributors = re.sub(r'\'', '', contributors) 
#     musical_work['contributors'] = contributors
#     util.csv.write_dict_as_csv(name='work_metadata', _dict=musical_work, dest=app.config['DOWNLOAD_FOLDER'])
#     return send_from_directory(app.config['DOWNLOAD_FOLDER'], 'work_metadata.csv', as_attachment=True)

@app.route('/api/musical_work', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file',
                                filename=filename))
    #     # Return 201 CREATED
    #     return "", 201
    #     if "/" in filename:
    #         # Return 400 BAD REQUEST
    #         abort(400, "no subdirectories directories allowed")
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
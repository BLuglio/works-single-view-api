from flask_restful import Resource, reqparse, request, fields, marshal_with, marshal
from flask import current_app as app, after_this_request, jsonify, abort, send_from_directory, make_response
import json
import re
import util.csv
import util.processor
from .model import MusicalWork
from werkzeug.utils import secure_filename
import os

class MusicalWorkResource(Resource):

    #############################################
    # every new field must be added here, otherwise it won't be returned in the response
    
    musical_work_fields = {
        'id': fields.Integer,
        'iswc': fields.String,
        'contributors': fields.List(fields.String),
        'title': fields.String(),
        'created_at': fields.String,
        'modified_at': fields.String,
        'download': fields.String,
        'upload': fields.String
    }

    musical_works_fields = {
        'id': fields.Integer,
        'iswc': fields.String,
        'url': fields.String
    }

    #############################################

    __model__ = MusicalWork()

    __processor__ = util.processor.Processor()

    def get(self, iswc=None):
        if 'upload' not in request.base_url:
            if iswc:
                # get single one
                res = self.__model__.get_by_iswc(iswc)
                if len(res) > 0:
                    # csv export
                    if 'download' in request.base_url:
                        return self.export_csv(res)
                    else:
                        res_new = [self.add_resource_url(item, {'download': f"{request.base_url}/download", 'upload': f"{request.base_url}/upload"}) for item in res]
                        return marshal(res_new, self.musical_work_fields), 200
                abort(404, description="Resource not found")
            else:
                # get all
                res = self.__model__.get_all()
                res_new = [self.add_resource_url(item, {'url': f"{request.base_url}/{item['iswc']}"}) for item in res]
                return marshal(res, self.musical_works_fields), 200
        abort(405, description="Method not allowed")
    
    def post(self, iswc):
        if len(request.files) == 0:
            abort(400, "no file part")
        file = request.files['file']
        if file:
            if file.filename == '':
                abort(400, "no selected file")
            if self.allowed_file(file.filename):
                try:
                    filename = secure_filename(file.filename)
                    if "/" in filename:
                        abort(400, "no subdirectories directories allowed")
                    _filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(_filename)
                except(Exception) as e:
                    print(e)
                    abort(400, "invalid file")
                data = self.__processor__.process(_filename, iswc)
                if len(data) > 0:
                    self.__model__.insert(data)
                    os.remove(_filename)
                    # Return 201 CREATED
                    message = {"message": f"{filename} uploaded successfully!", "url": request.base_url.replace("/upload","")}
                    response = app.response_class(response=json.dumps(message),
                                  status=201,
                                  mimetype='application/json')
                    return response
                else:
                    abort(400, "invalid file")
            abort(400, "file not allowed")
        abort(400, "file not found") 

    def add_resource_url(self, item, resource_dict):
        new_item = item
        for r in resource_dict.keys():
            new_item[r] = resource_dict[r]
        return new_item
    
    def allowed_file(self, filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    def export_csv(self, res):
        musical_work = res[0] # exactly one record has been fetched
        musical_work = dict(musical_work)
        # formatting the contributors as the string in works_metadata file
        contributors = str(musical_work['contributors']).replace('[','').replace(']','').replace(', ', '|')
        contributors = re.sub(r'\'', '', contributors) 
        musical_work['contributors'] = contributors
        _filename = musical_work['iswc'] + '_metadata.csv'
        util.csv.write_dict_as_csv(name=_filename, _dict=musical_work, dest=app.config['DOWNLOAD_FOLDER'])
        return send_from_directory(app.config['DOWNLOAD_FOLDER'], _filename, as_attachment=False)


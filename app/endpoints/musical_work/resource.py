from flask_restful import Resource, reqparse, request, fields, marshal_with, marshal
from flask import current_app as app, after_this_request, jsonify, abort, send_from_directory, make_response
import json
import re
import util.csv
from .model import MusicalWork

class MusicalWorkResource(Resource):

    musical_work_fields = {
        'iswc': fields.String,
        'contributors': fields.String,
        'title': fields.String
    }

    musical_works_fields = {
        'iswc': fields.String,
        'url': fields.String
    }

    __model__ = MusicalWork()

    def get(self, iswc=None):
        if iswc:
            res = self.__model__.get_by_iswc(iswc)
            if len(res) > 0:
                if 'download' in request.base_url:
                    musical_work = res[0]
                    ##### reformat result
                    musical_work = dict(musical_work)
                    contributors = str(musical_work['contributors']).replace('[','').replace(']','').replace(', ', '|')
                    contributors = re.sub(r'\'', '', contributors) 
                    musical_work['contributors'] = contributors
                    _filename = musical_work['iswc'] + '_metadata.csv'
                    util.csv.write_dict_as_csv(name=_filename, _dict=musical_work, dest=app.config['DOWNLOAD_FOLDER'])
                    return send_from_directory(app.config['DOWNLOAD_FOLDER'], _filename, as_attachment=False))
                else:
                    res_new = [self.add_resource_url(item, {'csv': f"/musical_works/{item['iswc']}/download"}) for item in res]
                    return res_new
            else:
                abort(404, description="Resource not found")
        else:
            res = self.__model__.get_all()
            res_new = [self.add_resource_url(item, {'url': f"/musical_works/{item['iswc']}"}) for item in res]
            return list(res_new)

#     if('/download' in response.base_url):
#         try:

#     return response

    # def post(self, iswc=None):


    def add_resource_url(self, item, resource_dict):
        new_item = item
        for r in resource_dict.keys():
            new_item[r] = resource_dict[r]
        return new_item
    
    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


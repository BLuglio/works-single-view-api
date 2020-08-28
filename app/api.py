from flask import current_app as app
from flask_restful import Api

api = Api(app)
api.prefix = '/api'

from endpoints.musical_work.resource import MusicalWorkResource

api.add_resource(MusicalWorkResource, '/musical_works', '/musical_works/<string:iswc>', '/musical_works/<string:iswc>/download')
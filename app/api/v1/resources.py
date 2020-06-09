import logging

from flask_restful import Resource, Api

api = Api(prefix="/api/v1")

LOG = logging.getLogger(__name__)


@api.resource('/version')
class Version(Resource):
    def get(self):
        with open('app/version') as f:
            return f.read()


"""
.. module:: api
   :synopsis: The API for the Flask APP generator located here
.. moduleauthor:: Alexey Suponin
"""

import logging

from flask_restful import Resource, Api, reqparse

api = Api(prefix="/api/v1")

LOG = logging.getLogger(__name__)

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('packages')


@api.resource('/version')
class Version(Resource):
    def get(self):
        """
            **Get current version of app**
            :return: string
            - Example::
                curl  http://127.0.0.1:5000/api/v1/version
            - Expected Success Response::
                FlaskCMS 1.0
        """
        with open('app/version') as f:
            return f.read()


@api.resource('/project')
class Project(Resource):
    def post(self):
        """
            **Create anonymous project and get link to it**
            :return: string
            - Example::
                 curl -X POST -d"name=test&packages=main,auth" http://127.0.0.1:5000/api/v1/project
            - Expected Success Response::
               {
                    "name": "test",
                    "packages": "main,auth"
                }

        """
        args = parser.parse_args()
        return args

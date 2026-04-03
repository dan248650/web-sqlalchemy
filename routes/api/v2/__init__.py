from flask_restful import Api
from routes.api.v2.users_resource import UsersListResource, UsersResource


def init_api_v2(app):
    api = Api(app, prefix='/api/v2')

    api.add_resource(UsersListResource, '/users')
    api.add_resource(UsersResource, '/users/<int:user_id>')

    return api

from flask import Flask
from flask_restful import Api

from wts_api import session
from wts_api.resources import task
from wts_api.settings import Settings


def start_api(conf=None):
    """Creates the Flask application and registers its resources
    """
    app = Flask(__name__)
    app.config.update(Settings)

    api = Api(app)
    api.add_resource(task.Task, '/task', '/task/<string:uuid>')
    api.add_resource(task.TaskList, '/tasks')
    api.add_resource(task.Video, '/video/<string:uuid>')

    session.SessionScope.init_database()

    return app

from elasticsearch_dsl.connections import connections
from flask import Flask
from flask_restful import Api

from wts_api import session
from wts_api.resources import task, search
from wts_api.settings import Settings


def start_api():
    """Creates the Flask application and registers its resources
    """
    app = Flask(__name__)
    app.config.update(Settings)

    api = Api(app)
    api.add_resource(task.Task, '/task', '/task/<string:uuid>')
    api.add_resource(task.TaskList, '/tasks')
    api.add_resource(task.Video, '/video/<string:uuid>')
    api.add_resource(search.Search, '/search/<string:terms>')

    # Init database connection
    session.SessionScope.init_database()

    # Create the Elasticsearch connection
    connections.create_connection(hosts=[Settings.get('SEARCH_HOST')
                                         or 'localhost'],
                                  timeout=20)

    return app

from flask import Flask
from flask_restful import Api

from wts_api.resources import task


app = Flask(__name__)
app.config.from_object('wts_api.config.DevelopmentConfig')

api = Api(app)
api.add_resource(task.Task, '/task','/task/<string:uuid>')
api.add_resource(task.TaskList, '/tasks')
api.add_resource(task.Video, '/video/<string:uuid>')

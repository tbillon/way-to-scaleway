from flask import request
from flask_restful import fields, marshal, Resource

from wts_api.common import SessionScope
from wts_api.common.utils import valid_task, valid_uuid
from wts_db import models
from wts_worker import worker


task_fields = {
    'uuid': fields.String,
    'sub_date': fields.DateTime,
    'src_url': fields.String
}


class Task(Resource):
    def delete(self, uuid=None):
        if uuid is None:
            return {'error': 'No UUID provided'}, 400
        if not valid_uuid(uuid):
            return {'error': "'{}' is not a valid UUID".format(uuid)}, 400

        with SessionScope() as session:
            task = session.query(models.Task).filter(models.Task.uuid == uuid).first()
            if task is None:
                return {'error': "'{}' unknown task".format(uuid)}, 404
            session.delete(task)
            session.commit()
            return marshal(task, task_fields)


    def get(self, uuid=None):
        if uuid is None:
            return {'error': 'No UUID provided'}, 400
        if not valid_uuid(uuid):
            return {'error': "'{}' is not a valid UUID".format(uuid)}, 400

        with SessionScope() as session:
            task = session.query(models.Task).filter(models.Task.uuid == uuid).first()
            if task is None:
                return {'error': "'{}' unknown task".format(uuid)}, 404
            return marshal(task, task_fields)


    def post(self):
        data = request.get_json(force=True)
        if not valid_task(data):
            return {'error': "'{}' invalid task".format(data)}, 400

        with SessionScope() as session:
            task = models.Task(data['url'])
            session.add(task)
            session.commit()
            worker.video_download.delay(task.uuid)
            return marshal(task, task_fields, envelope='task')


class TaskList(Resource):
    def get(self):
        with SessionScope() as session:
            tasks = session.query(models.Task).all()
            return marshal(tasks, task_fields, envelope='tasks')

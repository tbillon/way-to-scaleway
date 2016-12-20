from flask import request, send_from_directory
from flask_restful import fields, Resource

from wts_api.common import SessionScope
from wts_api.common.utils import my_marshal, valid_task, valid_uuid
from wts_db import models, config
from wts_worker import worker


class TaskStatusField(fields.Raw):
    status = {
        0: 'pending',
        1: 'started',
        2: 'finished',
        3: 'error'
    }

    def format(self, value):
        return self.status[value]


task_fields = {
    'uuid': fields.String,
    'sub_date': fields.DateTime,
    'upd_date': fields.DateTime,
    'src_url': fields.String,
    # 'dst_url': fields.String,
    'dst_url': fields.Url('video', absolute=True),
    'status': TaskStatusField,
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
            return my_marshal(task, task_fields)


    def get(self, uuid=None):
        if uuid is None:
            return {'error': 'No UUID provided'}, 400
        if not valid_uuid(uuid):
            return {'error': "'{}' is not a valid UUID".format(uuid)}, 400

        with SessionScope() as session:
            task = session.query(models.Task).filter(models.Task.uuid == uuid).first()
            if task is None:
                return {'error': "'{}' unknown task".format(uuid)}, 404
            return my_marshal(task, task_fields)


    def post(self):
        data = request.get_json(force=True)
        if not valid_task(data):
            return {'error': "'{}' invalid task".format(data)}, 400

        with SessionScope() as session:
            task = models.Task(data['url'])
            session.add(task)
            session.commit()
            chain = worker.video_download.s(task.uuid) | worker.video_move.s(task.uuid)
            chain()
            return my_marshal(task, task_fields, envelope='task')


class TaskList(Resource):
    def get(self):
        with SessionScope() as session:
            tasks = session.query(models.Task).all()
            return my_marshal(tasks, task_fields, envelope='tasks')


class Video(Resource):
    def get(self, uuid=None):
        if uuid is None:
            return {'error': 'No UUID provided'}, 400
        if not valid_uuid(uuid):
            return {'error': "'{}' is not a valid UUID".format(uuid)}, 400

        with SessionScope() as session:
            t = session.query(models.Task).filter(models.Task.uuid == uuid).first()
            if t is None:
                return {'error': "'{}' unknown video".format(uuid)}, 404
        return send_from_directory(config.INCOMING_VIDEO_URI, t.dst_url)

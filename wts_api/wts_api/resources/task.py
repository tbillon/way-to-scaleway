"""
SW tutorial
~~~~~~~~~~~

Task REST functions
"""
from flask import request, send_from_directory
from flask_restful import abort, fields, marshal, Resource

from sqlalchemy import and_

from wts_api.settings import Settings
from wts_api.session import SessionScope
from wts_api.utils import valid_task, valid_uuid
from wts_api.worker import video_download_chain_task
from wts_db import models


def abort_on_invalid_uuid(uuid):
    if uuid is None:
        abort(400, message="No UUID provided")
    if not valid_uuid(uuid):
        abort(400, message="'{}' is not a valid UUID".format(uuid))


class Task(Resource):
    task_delete_fields = {'uuid': fields.String, }
    task_get_fields = {'uuid': fields.String, }
    task_post_fields = {'uuid': fields.String,
                        'sub_date': fields.DateTime,
                        'src_url': fields.String, }

    def delete(self, uuid=None):
        abort_on_invalid_uuid(uuid)

        with SessionScope() as ssc:
            task = ssc.query(models.Task).filter(models.Task.uuid == uuid).first()
            if task is None:
                return {'error': "'{}' unknown task".format(uuid)}, 404
            ssc.delete(task)
            ssc.commit()
            return marshal(task, self.task_delete_fields)

    def get(self, uuid=None):
        abort_on_invalid_uuid(uuid)

        with SessionScope() as ssc:
            task = ssc.query(models.Task).filter(models.Task.uuid == uuid).first()
            if task is None:
                return {'error': "'{}' unknown task".format(uuid)}, 404
            return marshal(task, self.task_get_fields)

    def post(self):
        data = request.get_json(force=True)
        if not valid_task(data):
            return {'error': "'{}' invalid task".format(data)}, 400

        with SessionScope() as ssc:
            task = models.Task(data['url'])
            ssc.add(task)
            ssc.commit()
            video_download_chain_task(task.uuid)
            return marshal(task, self.task_post_fields, envelope='task')


class TaskList(Resource):
    task_list_fields = {
        'uuid': fields.String,
        'sub_date': fields.DateTime,
        'src_url': fields.String,
        'dst_url': fields.String,
    }

    def get(self):
        with SessionScope() as ssc:
            tasks = ssc.query(models.Task).all()
            return marshal(tasks, self.task_list_fields, envelope='tasks')


class Video(Resource):
    """Send a previously downloaded video
    """
    def get(self, uuid=None):
        abort_on_invalid_uuid(uuid)
        with SessionScope() as ssc:
            task = ssc.query(models.Task).filter(and_(models.Task.uuid == uuid,
                                                      models.Task.dst_url != None)).first()
            if task is None:
                return {'error': "'{}' unknown video".format(uuid)}, 404
        return send_from_directory(Settings.get('OUTPUT_DIRECTORY'), task.dst_url)

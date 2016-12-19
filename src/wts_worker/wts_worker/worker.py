from time import sleep

from celery import Celery

from wts_db import models
from wts_worker import DatabaseTask


app = Celery('tasks', backend='rpc://', broker='amqp://localhost')
#app.conf.task_serializer = 'json'


@app.task(base=DatabaseTask, bind=True, ignore_result=True)
def video_download(self, uuid):
    t = self.session.query(models.Task).filter(models.Task.uuid == uuid).one()
    sleep(5)

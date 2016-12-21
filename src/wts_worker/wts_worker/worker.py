from __future__ import unicode_literals
import os
from time import sleep

from celery import Celery
import youtube_dl

from wts_db.wts_db import models, config
from wts_worker.wts_worker import DatabaseTask


app = Celery('tasks', backend='rpc://', broker='amqp://localhost')
#app.conf.task_serializer = 'json'


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


@app.task(base=DatabaseTask, bind=True, ignore_result=False)
def video_download(self, uuid):
    t = self.session.query(models.Task).filter(models.Task.uuid == uuid).one()

    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(id)s.%(ext)s',
        'quiet': True,
        'logger': MyLogger(),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            t.status = 1
            self.session.commit()
            res = ydl.extract_info(t.src_url,force_generic_extractor=True )
            if 'entries' in res:
                # Can be a playlist or a list of videos
                video = res['entries'][0]
            else:
                # Just a video
                video = res
                return {'file': ydl_opts['outtmpl'] % video, 'title': res['title']}
        except youtube_dl.DownloadError as e:
            t.status = 3
            self.session.commit()
            raise e


@app.task(base=DatabaseTask, bind=True, ignore_result=True)
def video_move(self, properties, uuid):
    if not os.path.isdir(config.INCOMING_VIDEO_URI):
        os.makedirs(config.INCOMING_VIDEO_URI)
    os.rename(properties['file'], os.path.join(config.INCOMING_VIDEO_URI, properties['file']))
    t = self.session.query(models.Task).filter(models.Task.uuid == uuid).one()
    t.dst_url = properties['file']
    if properties['title'] is not None:
        t.title = properties['title']
    t.status = 2
    self.session.commit()

"""
SW tutorial
~~~~~~~~~~~

SW Celery workers
"""
from __future__ import unicode_literals
import os

import youtube_dl

from wts_worker.app import app
from wts_db import models
from wts_worker import DatabaseTask
from wts_worker.settings import Settings


class MyLogger(object):
    """Youtube-dl logger
    """
    def debug(self, msg):
        """Ignore debug messages"""
        pass

    def warning(self, msg):
        """Ignore warning messages"""
        pass

    def error(self, msg):
        """Display error messages"""
        print msg


@app.task(base=DatabaseTask, bind=True, ignore_result=False)
def video_download(self, uuid):
    t = self.session.query(models.Task).filter(models.Task.uuid == uuid).one()

    ydl_opts = {
        'format': 'best',
        'outtmpl': '{}%(id)s.%(ext)s'.format(Settings.get('OUTPUT_DIRECTORY')),
        'quiet': not Settings.get('DEBUG'),
        'logger': MyLogger(),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            res = ydl.extract_info(t.src_url,force_generic_extractor=True )
            if 'entries' in res:
                # Can be a playlist or a list of videos
                video = res['entries'][0]
            else:
                # Just a video
                video = res
            return {'file': ydl_opts['outtmpl'] % video, 'title': res['title']}
        except youtube_dl.DownloadError as e:
            raise e


@app.task(base=DatabaseTask, bind=True, ignore_result=True)
def video_register_title(self, video, uuid):
    task = self.session.query(models.Task).filter(models.Task.uuid == uuid).one()
    task.dst_url = video.get('file')
    if video.get('title') is not None:
        task.title = video.get('title')
    self.session.commit()

# Way to SW

The purpose of this simple project is to learn most of the parts used at SW.

We'll build a simple API to download videos from Youtbe.

API endpoints:

```
curl http://myapi.com/download -H 'Content-Type: application/json' -d '{"url": "http://youtube.com/....."}'

    HTTP/200 OK

    {
        "task": "<UUID>"
    }


curl http://myapi.com/tasks/<UUID>

    HTTP/200 OK

    {
        "status": "pending"
    }

curl http://myapi.com/tasks/<UUID>

    HTTP/200 OK

    {
        "status": "ok"
        "url": "http://myapi.com/videos/<url de la video>"
    }


curl http://myapi.com/videos/

    HTTP/200 OK

    {
        "videos": [
            {"url": "http://myapi.com", "orig_url": "http://youtube.com/....."}
        ]
    }

```


## Step 1

Build the base system.

### Database schema

At least :
	Table videos
		uuid UUID primary key
		src_url VARCHAR
		url VARCHAR

### Features

Things to do in no particular order:

	- A PostgreSQL database contains all the videos
	- Videos are stored on the file system
	- REST API build upon
      [flask-restful](http://flask-restful.readthedocs.io/)
	- RabbitMQ + [Celery](http://www.celeryproject.org/) for all asynchronous
      operations
	- API parameters validation with
      [Voluptuous](http://alecthomas.github.io/voluptuous/)
	- Data serialization with
      [marshal](http://flask-restful-cn.readthedocs.io/en/0.3.4/fields.html)
	- Packaging with `setuptools` (look at `console_scripts`)
	- Everything must work inside a virtualenv


## Step 2

Add database versionning with
[http://alembic.zzzcomputing.com/en/latest/](Alembic).

Given an empty database, doing an `alembic upgrade head` must create all the
database tables.

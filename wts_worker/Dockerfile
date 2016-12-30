FROM python:2.7

ADD . /code
ENV CREDENTIALS /etc/credentials.yaml
WORKDIR /code

RUN apt-get install -y \
    libyaml-dev \
    libyaml-0-2 \
    libpq-dev \
    libpq5 \
    && pip install -r wts_db/requirements.txt \
    && pip install -r wts_worker/requirements.txt

RUN pip install wts_db/ \
    && pip install wts_worker/

CMD ["start-wts-worker", "worker", "-A", "wts_worker.app"]

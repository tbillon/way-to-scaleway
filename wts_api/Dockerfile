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
    && pip install wts_db/

RUN  pip install -r wts_api/requirements.txt \
     && pip install wts_api/

EXPOSE 5000

CMD ["start-wts-api"]

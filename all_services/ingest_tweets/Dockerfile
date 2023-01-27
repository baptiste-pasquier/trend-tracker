FROM python:3.10.9-alpine

# copy project
COPY . /usr/src/app

# set working directory
WORKDIR /usr/src/app

RUN pip3 install .
RUN pip3 install -r all_services/ingest_tweets/requirements.txt

CMD ["python", "all_services/ingest_tweets/app.py"]

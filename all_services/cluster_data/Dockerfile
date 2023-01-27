FROM python:3.10.9-slim

# copy project
COPY . /usr/src/app

# set working directory
WORKDIR /usr/src/app

RUN pip3 install .
RUN pip3 install -r all_services/cluster_data/requirements.txt

CMD ["python", "all_services/cluster_data/app.py"]

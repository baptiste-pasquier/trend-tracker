FROM python:3.10.9-alpine

# copy project
COPY . /usr/src/app

# set working directory
WORKDIR /usr/src/app

RUN pip3 install .
RUN pip3 install -r all_services/tsf_data/requirements.txt

CMD ["python", "all_services/tsf_data/app.py"]

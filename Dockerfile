# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:3.6-slim-stretch

# If you prefer miniconda:
#FROM continuumio/miniconda3

LABEL Name=medicine Version=0.0.1

WORKDIR /medicine
ADD requirements.txt /medicine/requirements.txt

# Using pip:
# COPY sources.list /etc/apt/sources.list

RUN apt-get update -qq && \
    apt-get install -qq -y --no-install-recommends \
        git gcc g++ make default-libmysqlclient-dev && \
    apt-get autoremove -qq -y --purge && \
    rm -rf /var/cache/apt /var/lib/apt/lists

RUN pip install --no-cache-dir -r requirements.txt -i http://mirrors.cloud.tencent.com/pypi/simple --trusted-host mirrors.cloud.tencent.com

RUN adduser --disabled-password --gecos '' appuser

EXPOSE 8000

# Using pipenv:
#RUN python3 -m pip install pipenv
#RUN pipenv install --ignore-pipfile
#CMD ["pipenv", "run", "python3", "-m", "medicine"]

# Using miniconda (make sure to replace 'myenv' w/ your environment name):
#RUN conda env create -f environment.yml
#CMD /bin/bash -c "source activate myenv && python3 -m medicine"

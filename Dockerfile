# Use an official Python runtime as the base image
FROM python:3.10.6

WORKDIR /python-docker

# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt

COPY . .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev


CMD [ "python3", "main.py"]

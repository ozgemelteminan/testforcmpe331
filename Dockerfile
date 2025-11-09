FROM python:3.11-slim
RUN apt-get update && apt-get install -y build-essential libffi-dev python3-dev
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code/
EXPOSE 8000
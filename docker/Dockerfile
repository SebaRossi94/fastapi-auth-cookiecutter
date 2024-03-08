FROM tiangolo/uvicorn-gunicorn:python3.11

COPY . /app

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry
RUN pip install debugpy

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt
RUN pip install -r requirements.txt

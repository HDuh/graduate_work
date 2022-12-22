FROM python:3.11-slim

# set environment variables
ENV PYTHONPATH "${PYTHONPATH}:/app/"
ENV PATH="${PATH}:/root/.local/bin"


COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir\
    && pip install -r requirements.txt --no-cache-dir


RUN mkdir /app
WORKDIR /app/

EXPOSE 8001
ENTRYPOINT python ./src/main.py
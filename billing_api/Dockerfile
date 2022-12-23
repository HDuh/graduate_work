FROM python:3.11-slim

# set environment variables
ENV PYTHONPATH "${PYTHONPATH}:/app/"
ENV PATH="${PATH}:/root/.local/bin"


COPY requirements.txt .
COPY entrypoint.sh .
RUN pip install --upgrade pip --no-cache-dir\
    && pip install -r requirements.txt --no-cache-dir


RUN mkdir /app
WORKDIR /app/
COPY . .

RUN apt update && apt install -y netcat && chmod +x ./entrypoint.sh
ENTRYPOINT sh ./entrypoint.sh
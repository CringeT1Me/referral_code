FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /users_service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000


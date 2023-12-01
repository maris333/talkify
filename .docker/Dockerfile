FROM python:3.11-alpine
WORKDIR /talkify
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ .
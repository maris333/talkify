FROM python:3.11-alpine
ENV PYTHONPATH=.
WORKDIR /talkify
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src
COPY tests/ ./tests
FROM --platform=linux/arm64 python:3.8-slim-buster as build
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app/
CMD ["python3", "main.py"]

# Use an official Python runtime as a parent image
FROM python:3.11-slim-bullseye

# Use "bash" as replacement for    "sh"
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /code
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./scripts/* /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

RUN source ./scripts/export_vars.sh

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

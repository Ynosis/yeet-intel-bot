# Using lightweight alpine image
FROM python:3.13.0a4-alpine

# Set working directory
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "gno.py"]
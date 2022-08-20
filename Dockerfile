FROM python:3.9.4-alpine
# Additional package installation
RUN apk --no-cache add curl

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src .

HEALTHCHECK NONE
CMD [ "python", "main.py" ]

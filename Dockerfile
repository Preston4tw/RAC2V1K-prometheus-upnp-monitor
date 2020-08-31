FROM python:3.8-alpine

# Needed for lxml, needed by upnpclient
RUN apk update && apk add libxslt-dev libxml2-dev gcc musl-dev

WORKDIR /app

# If requirements.txt doesn't change, cache it
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY upnpRouterMonitor.py .

CMD ["python", "upnpRouterMonitor.py"]
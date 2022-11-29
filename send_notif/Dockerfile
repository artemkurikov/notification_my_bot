FROM python:3.8-slim-buster

WORKDIR /send_notif

RUN apt-get update && \
    apt-get clean && rm -rf /var/lib/apt/lists/* 

COPY requirements.txt .
COPY send_notif.py . 

RUN mkdir /send_notif/conf
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3.8", "send_notif.py"]
#EXPOSE 8080

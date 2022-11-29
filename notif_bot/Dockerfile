FROM python:3.8-slim-buster

WORKDIR /notif_bot

RUN apt-get update && \
    apt-get clean && rm -rf /var/lib/apt/lists/* 

COPY requirements.txt .
COPY notif_bot.py . 

RUN mkdir /notif_bot/conf
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3.8", "notif_bot.py"]
#EXPOSE 8080

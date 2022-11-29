FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential gcc && \
    apt-get install gunicorn3 -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/* 

COPY requirements.txt .
COPY app.py .

RUN pip3 install --no-cache-dir -r requirements.txt
RUN echo "[]" >> notif.json
RUN echo "[]" >> user_list

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
EXPOSE 8080

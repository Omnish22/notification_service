FROM python:3.9-slim

WORKDIR /worker

COPY ./requirements.txt /worker/requirements.txt
RUN pip3 install -r /worker/requirements.txt

COPY . .

CMD [ "celery", "-A", "notification_service.celery", "worker", "--loglevel=info", "--queues=email_queue" , "--concurrency=4"]
import os

from django.conf import settings

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification_service.settings')

app = Celery('notification_service', broker='pyamqp://guest@rabbitmq//', backend='redis://redis:6379/0')

app.conf.task_queues={
    'sms_queue':{
        'exchange':'sms_exchange',
        'routing_key':'sms'
    },
    'email_queue':{
        'exchange':'email_exchange',
        'routing_key':'email'
    }
}

app.conf.task_routes = {
    'workers.sms.tasks.send_sms_task': {'queue': 'sms_queue'},
    'workers.email.tasks.send_email_task': {'queue': 'email_queue'},
}

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
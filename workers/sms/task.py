from celery import shared_task
from twilio.rest import Client
import os
from notification.models import Notification, Tasks

@shared_task(queue="sms_queue")
def send_sms_task():
    try:
        pending_tasks = Tasks.objects.filter(status=Notification.Status.PENDING)


        for task in pending_tasks:
            notificiation = Notification.objects.get(id=task.notification_id.id)
            task.status=Notification.Status.IN_PROGRESS
            task.save()
            notificiation.status=Notification.Status.IN_PROGRESS
            notificiation.save()

            account_sid = os.getenv("ACCOUNTSID")
            auth_token = os.getenv("AUTHTOKEN")
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                messaging_service_sid= os.getenv("MESSAGINGSERVICESID"),
                body=notificiation.content.get("msg"),
                to=os.getenv("TO")
            )
            notificiation = Notification.objects.get(id=task.notification_id.id)
            task.status=Notification.Status.SENT
            task.save()
            notificiation.status=Notification.Status.SENT
            notificiation.save()
    except Exception as e:
        notificiation = Notification.objects.get(id=task.notification_id.id)
        task.status=Notification.Status.FAILED
        task.save()
        notificiation.status=Notification.Status.FAILED
        notificiation.save()
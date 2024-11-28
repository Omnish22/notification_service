from notification.models import Tasks, Notification
import smtplib
from email.message import EmailMessage
import os
import ssl
from celery import shared_task

@shared_task(queue="email_queue")
def send_email_task():
    try:

        # FETCH THE TASK AND ASSOCIATED WITH NOTIFICATION
        pending_task = Tasks.objects.filter(status=Notification.Status.PENDING)

        context = ssl.create_default_context()
        # UPDATE TASK OBJECT TO INPROGRESS
        for task in pending_task:
            em = EmailMessage()
            em['From'] = os.getenv('MAILSENDER') 
            em['Subject'] = "Alert Notification"
            sending_to = ["omnish22@gmail.com"]
            em['To'] = ", ".join(sending_to)

            notification = Notification.objects.get(id=task.notification_id.id)
            task.status = Notification.Status.IN_PROGRESS
            task.save()
            notification.status =  Notification.Status.IN_PROGRESS
            notification.save()

            body = f"{notification.content.get('msg')}"
            em.set_content(body)

            # EMAIL SENDING 
            with smtplib.SMTP_SSL(os.getenv('MAILSERVICE'), os.getenv('MAILPORT'), context=context) as smtp:
                smtp.login(os.getenv('MAILSENDER'),os.getenv('MAILPASSWORD'))
                smtp.send_message(em)
            task.status = Notification.Status.SENT
            task.save()
            notification.status =  Notification.Status.SENT
            notification.save()
    except Exception as e:
        task.status = Notification.Status.FAILED
        task.save()
        notification.status =  Notification.Status.FAILED
        notification.save()
        raise e

from notification.models import Tasks, Notification
import smtplib
from email.message import EmailMessage
import os
import ssl

def send_email():
    try:
        em = EmailMessage()
        em['From'] = os.getenv('MAILSENDER') 
        em['Subject'] = "Alert Notification"
        sending_to = ["omnish22@gmail.com"]
        em['To'] = ", ".join(sending_to)

        # FETCH THE TASK AND ASSOCIATED WITH NOTIFICATION
        pending_task = Tasks.objects.filter(status=Notification.Status.PENDING)

        context = ssl.create_default_context()
        # UPDATE TASK OBJECT TO INPROGRESS
        for task in pending_task:
            notification = Notification.objects.get(id=task.notification_id)
            task.status = Notification.Status.IN_PROGRESS
            task.save()

            body = f"{notification.content.get('msg')}"
            em.set_content(body)

            # EMAIL SENDING 
            with smtplib.SMTP_SSL(os.getenv('MAILSERVICE'), os.getenv('MAILPORT'), context=context) as smtp:
                smtp.login(os.getenv('MAILSENDER'),os.getenv('MAILPASSWORD'))
                smtp.send_message(em)
    except:
        task.status = Notification.Status.FAILED

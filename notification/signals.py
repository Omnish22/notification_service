from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, Tasks
from workers.email.task import send_email_task
from workers.sms.task import send_sms_task

@receiver(post_save, sender=Notification)
def create_task_on_notification(sender, instance, created, **kwargs):
    if created and instance.status == Notification.Status.PENDING:
        task = Tasks.objects.create(
            notification_id=instance,
            status=Notification.Status.PENDING,
            result=instance.content
        )
        if instance.type=='email':
            send_email_task.delay()
        elif instance.type=='sms':
            send_sms_task.delay()
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your models here.
class Type(models.TextChoices):
    EMAIL='email'
    SMS='sms'
    PUSH='push'

class Status(models.TextChoices):
    PENDING='pending'
    SENT='sent'
    FAILED='failed'

# NOTIFICATIONS
class Notification(models.Model):
    # Create your models here.
    class Type(models.TextChoices):
        EMAIL='email'
        SMS='sms'
        PUSH='push'

    class Status(models.TextChoices):
        PENDING='pending'
        IN_PROGRESS = 'inprogress'
        SENT='sent'
        FAILED='failed'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification')
    type = models.CharField(max_length=20, choices=Type.choices)
    status = models.CharField(max_length=20, choices=Status.choices)
    content = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Notification {self.id} for {self.user.email}"
    
    def clean(self):
        if self.type == 'sms' and 'phone_number' not in self.metadata:
            super().clean()
            raise ValidationError({"metadata":"SMS notification require phone_number"})
        if self.type == 'push' and 'device_id' not in self.metadata:
            raise ValidationError({"metadata":"PUSH notification require device_id"})


# NOTIFICATION PREFRENCES
class Tasks(models.Model):
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification_id = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(
        max_length=20,
        choices=Notification.Status.choices,
        default=Notification.Status.PENDING
    )
    result = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)


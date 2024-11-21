from django.contrib import admin
from .models import Notification, Tasks
# Register your models here.

admin.site.register(Notification)
admin.site.register(Tasks)
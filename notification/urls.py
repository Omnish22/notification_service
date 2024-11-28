from django.urls import path
from .views import NotificationView, TaskView

urlpatterns = [
    path('notification', NotificationView.as_view(), name='notification'),
    path('task', TaskView.as_view(), name='task'),
]

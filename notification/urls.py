from django.urls import path
from .views import NotificationView

urlpatterns = [
    path('notification', NotificationView.as_view(), name='notification'),
]

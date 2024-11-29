from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import SerializeNotification, SerializeTasks
from rest_framework.views import Response
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
import time

# Create your views here.

class NotificationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        time.sleep(10)
        try:
            # CREATE ENTRY IN DB
            serializer = SerializeNotification(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            

        except serializers.ValidationError as e:
            return Response({"error":f"Invalid Data: {e} and data: {request.data}"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

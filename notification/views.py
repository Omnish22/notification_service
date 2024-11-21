from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import SerializeNotification
from rest_framework.views import Response
from rest_framework import serializers, status

# Create your views here.

class NotificationView(APIView):
    def post(self, request):
        try:
            # CREATE ENTRY IN DB
            serializer = SerializeNotification(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except serializers.ValidationError:
            return Response({"error":"Invalid Data"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
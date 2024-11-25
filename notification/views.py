from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import SerializeNotification
from rest_framework.views import Response
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny

# Create your views here.

class NotificationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print('notification')
        try:
            print('data: ',request.data)
            # CREATE ENTRY IN DB
            serializer = SerializeNotification(data=request.data)
            print("serializer: ", serializer)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except serializers.ValidationError as e:
            print("ERROR COMES", request.data)
            return Response({"error":f"Invalid Data: {e} and data: {request.data}"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
from rest_framework import serializers
from .models import Notification, Tasks
from django.contrib.auth import get_user_model

User = get_user_model()

class SerializeNotification(serializers.ModelSerializer):
    user = serializers.EmailField()

    class Meta:
        model = Notification
        fields = ['user', 'type', 'status', 'content', 'metadata']

    def validate_user(self, email):
        """
        Validate that the provided email corresponds to an existing User.
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid user email. User does not exist.")

    def create(self, validated_data):
        """
        Override the create method to resolve the user from the email.
        """
        user_email = validated_data.pop('user')  # Pop the email value from data
        user = self.validate_user(user_email)   # Resolve the user instance
        return Notification.objects.create(user=user, **validated_data)
    

class SerializeTasks(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['notification_id', 'status', 'result']

    # def validate_notification_id(self, id):
    #     if not isinstance(id, serializers.UUIDField):
    #         raise serializers.ValidationError("Invalid NotificationID")
    #     return id
    
    def validate_status(self, status):
        valid_status = [status[0] for status in Notification.Status.choices]
        if status not in valid_status:
            raise serializers.ValidationError("Invalid Status")
        return status
    
    def validate_result(self, result):
        if not isinstance(result,dict):
            raise serializers.ValidationError("Invalid Result Type")
        return result
    
    def create(self, validated_data):
        return Tasks.objects.create(**validated_data)
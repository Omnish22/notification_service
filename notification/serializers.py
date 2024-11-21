from rest_framework import serializers
from .models import Notification, Tasks
from django.contrib.auth.models import User

class SerializeNotification(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['user_id', 'type', 'status', 'content']
    
    def validate_user_id(self, user_id):
        if not User.objects.filter(id=user_id):
            raise serializers.ValidationError("Invalid User ID. User Doesn't exist")
        return user_id
    
    def validate_type(self, type):
        # choice[0] corresponds to 'email', 'sms', 'push' (values stored in the database).
        # choice[1] corresponds to 'Email', 'SMS', 'Push' (human-readable labels).
        valid_types = [choice[0] for choice in Notification.Type.choices]
        if type not in valid_types:
            raise serializers.ValidationError("Invalid Type Entered")
        return type

    def validate_status(self, status):
        valid_status = [status[0] for status in Notification.Status.choices]
        if status not in valid_status:
            raise serializers.ValidationError("Invalid Status Entered")
        return status
    
    
    def validate_content(self, content):
        # Ensure the content field is a valid JSON object
        if not isinstance(content, dict):
            raise serializers.ValidationError("Content Must be JSON Format")
        
        # CHECK KEYS PRESENT IN CONTENT
        require_keys =[]
        for key in require_keys:
            if key not in content:
                raise serializers.ValidationError(f"Key is missing : {key}")
        return content
    

class SerializeTasks(serializers.ModelField):
    class Meta:
        model = Tasks
        fields = ['notification_id', 'status', 'result']

    def validate_notification_id(self, id):
        if not isinstance(id, serializers.UUIDField):
            raise serializers.ValidationError("Invalid NotificationID")
        return id
    
    def validate_status(self, status):
        valid_status = [status[0] for status in Notification.Status.choices]
        if status not in valid_status:
            raise serializers.ValidationError("Invalid Status")
        return status
    
    def validate_result(self, result):
        if not isinstance(result,dict):
            raise serializers.ValidationError("Invalid Result Type")
        return result
    
    
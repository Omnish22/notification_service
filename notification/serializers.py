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
    





    
# class SerializeNotification(serializers.ModelSerializer):

#     class Meta:
#         model = Notification
#         fields = ['user', 'type', 'status', 'content', 'metadata']
    
#     def validate_user(self, user):
#         print("USER ID: ", user)
#         if not User.objects.filter(id=user).exists():
#             raise serializers.ValidationError("Invalid User ID. User Doesn't exist")
#         return user
    
#     def validate_type(self, type):
#         # choice[0] corresponds to 'email', 'sms', 'push' (values stored in the database).
#         # choice[1] corresponds to 'Email', 'SMS', 'Push' (human-readable labels).
#         valid_types = [choice[0] for choice in Notification.Type.choices]
#         if type not in valid_types:
#             raise serializers.ValidationError("Invalid Type Entered")
#         return type

#     def validate_status(self, status):
#         valid_status = [status[0] for status in Notification.Status.choices]
#         if status not in valid_status:
#             raise serializers.ValidationError("Invalid Status Entered")
#         return status
    
#     def validate_metadata(self, metadata):
#         if not isinstance(metadata,dict):
#             raise serializers.ValidationError("Invalid metadata Type")
#         return metadata
    
    
#     def validate_content(self, content):
#         # Ensure the content field is a valid JSON object
#         if not isinstance(content, dict):
#             raise serializers.ValidationError("Content Must be JSON Format")
        
#         # CHECK KEYS PRESENT IN CONTENT
#         require_keys =[]
#         for key in require_keys:
#             if key not in content:
#                 raise serializers.ValidationError(f"Key is missing : {key}")
#         return content
    
#     def save(self, **kwargs):
#         # Perform validations before saving
#         validated_data = self.validated_data
        
#         # Extract data for further processing if needed
#         user_id = validated_data.get('user')
#         notification_type = validated_data.get('type')
#         status = validated_data.get('status')
#         content = validated_data.get('content')
#         metadata = validated_data.get('metadata')
        
#         # Additional logic before saving
#         print(f"Saving Notification for User ID: {user_id}")
#         print(f"Type: {notification_type}, Status: {status}, Metadata: {metadata}")
        
#         # Save the instance to the database
#         notification = Notification.objects.create(
#             user=user_id,  # This must already be validated as a valid ForeignKey
#             type=notification_type,
#             status=status,
#             content=content,
#             metadata=metadata,
#         )
        
#         # Return the saved notification instance
#         return notification
    

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
    

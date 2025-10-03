from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import User


class CustomRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, style={"input_type": "password"}) # this Field is just validation perpose

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "confirm_password", "country", "date_of_birth")
        write_only_fields = ( "confirm_password")
        
    def validate(self, fields):
        if fields["password"] != fields["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        
        try:
            validate_password(fields["password"])
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        
        return fields
    
    def create(self, validated_data):
        validated_data.pop("confirm_password", None)  # Remove confirm_password as it's not needed for user creation
        return User.objects.create_user(**validated_data)
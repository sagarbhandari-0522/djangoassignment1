from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError


class UserRegisterSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name",
                  "last_name", "email", "password", "password_confirmation"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, instance):
        if instance['password'] != instance['password_confirmation']:
            raise ValidationError({"message": "Both password must match"})

        if User.objects.filter(email=instance['email']).exists():
            raise ValidationError({"message": "Email already taken!"})

        if User.objects.filter(username=instance['username']).exists():
            raise ValidationError({"message": "Username already taken!"})

        return instance

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data)

        return user

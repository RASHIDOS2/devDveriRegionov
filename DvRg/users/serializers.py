from django.contrib.auth import get_user_model
from rest_framework import serializers
import uuid

class CustomUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'full_name', 'password']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user


class ProfileCustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['username', 'full_name']
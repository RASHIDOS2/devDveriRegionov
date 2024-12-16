from django.shortcuts import render
from rest_framework import viewsets, permissions, exceptions
from .serializers import CustomUserSerializer, ProfileCustomUserSerializer

from django.contrib.auth import get_user_model
# Create your views here


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]

class ProfileCustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfileCustomUserSerializer
    premission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user:
            user = get_user_model().objects.filter(pk=self.request.user.pk)
            if user is None:
                raise exceptions.AuthenticationFailed('Пользователь не найден')
            return user
from django.shortcuts import render
from rest_framework import viewsets, permissions, exceptions
from .serializers import CustomUserSerializer, ProfileCustomUserSerializer
from rest_framework.response import Response

from django.contrib.auth import get_user_model
# Create your views here


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]


class ProfileCustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = ProfileCustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        profile = self.get_queryset().get(pk=self.request.user.pk)
        serializer = self.get_serializer(profile)
        return Response({'user': serializer.data})
from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import CustomUserSerializer
from .models import CustomUser
# Create your views here


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]

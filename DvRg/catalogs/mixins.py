from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework import viewsets
from rest_framework.permissions import BasePermission


def my_response(results=None, status=status.HTTP_200_OK, headers=None, errors=None):
    return Response({
        'results': results,
        'errors': errors
    }, status, headers)


class CreateModelMixin:
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return my_response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListModelMixin:
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return my_response(self.get_paginated_response(serializer.data))

        serializer = self.get_serializer(queryset, many=True)
        return my_response(serializer.data)


class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return my_response(serializer.data)


class UpdateModelMixin:
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return my_response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin:
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return my_response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class IsOwnerOrAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST, ''PUT', 'DELETE']:
            # Разрешем обновлять и удалять свои запись только администратору
            return request.user and request.user.is_staff
        elif request.method in ['GET']:
            # Получать список могут только пользователи прошедшие аутентификацию
            return request.user and request.user.is_authenticated
        else:
            return True


class MyModelViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin,
                     viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrAdminUser]

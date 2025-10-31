from fcm_django.settings import FCM_DJANGO_SETTINGS as SETTINGS
from rest_framework import permissions, status
from rest_framework.response import Response

class DeviceViewSetMixin:
    lookup_field = 'registration_id'

    def create(self, request, *args, **kwargs):
        serializer = None
        is_update = False
        if SETTINGS.get('UPDATE_ON_DUPLICATE_REG_ID') and 'registration_id' in request.data:
            instance = self.queryset.model.objects.filter(registration_id=request.data['registration_id']).first()
            if instance:
                serializer = self.get_serializer(instance, data=request.data)
                is_update = True
        if not serializer:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if is_update:
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            if SETTINGS['ONE_DEVICE_PER_USER'] and self.request.data.get('active', True):
                FCMDevice.objects.filter(user=self.request.user).update(active=False)
            return serializer.save(user=self.request.user)
        return serializer.save()

    def perform_update(self, serializer):
        if self.request.user.is_authenticated:
            if SETTINGS['ONE_DEVICE_PER_USER'] and self.request.data.get('active', False):
                FCMDevice.objects.filter(user=self.request.user).update(active=False)
            return serializer.save(user=self.request.user)
        return serializer.save()
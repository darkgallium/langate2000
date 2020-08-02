from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.conf import settings
import logging
from markdown import Markdown

from ..serializers import *
from ..models import *

from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics

from modules import netcontrol


import random, json

class UserDetails(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserDeviceList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        u = User.objects.get(id=pk)

        if u == request.user or request.user.is_staff:
            # A normal user should only have access to the list of its devices,
            # So, we check that the request user matches the ID passed in parameter.
            # Admin users have the right to consult anyone's list of devices.

            qs = Device.objects.filter(user=u)
            serializer = UserDeviceSerializer(qs, many=True)

            return Response(serializer.data)

        else:
            raise PermissionDenied

class UserList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAdminUser,)

    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminUserDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        u = self.get_object()
        event_logger.info("User {} ({}) was removed by {}.".format(u.username, u.profile.role, request.user.username))
        return super().delete(request, args, kwargs)

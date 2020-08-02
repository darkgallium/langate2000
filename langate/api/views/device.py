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

class DeviceConnect(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user_devices = Device.objects.filter(user=request.user)
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR')

        if settings.ENABLE_NETCONTROL:
        # Checking if the device accessing the gate is already in user devices

            if not user_devices.filter(ip=client_ip).exists():

                #client_mac = network.get_mac(client_ip)

                r = netcontrol.query("get_mac", { "ip": client_ip })
                client_mac = r["mac"]

                if Device.objects.filter(mac=client_mac).count() > 0:

                    # If the device MAC is already registered on the network but with a different IP,
                    # * If the registered device is owned by the requesting user, we change the IP of the registered device.
                    # * If the registered device is owned by another user, we delete the old device and we register the new one.
                    # This could happen if the DHCP has changed the IP of the client.

                    # The following should never raise a MultipleObjectsReturned exception
                    # because it would mean that there are more than one devices
                    # already registered with the same MAC.

                    dev = Device.objects.get(mac=client_mac)

                    if request.user != dev.user:
                        dev.delete()

                        new_dev = Device(user=request.user, ip=client_ip)
                        new_dev.save()

                    else:
                        dev.ip = client_ip  # We edit the IP to reflect the change.
                        dev.save()

                elif len(user_devices) >= request.user.profile.max_device_nb:
                    # If user has too much devices already registered, then we can't connect the device to the internet.
                    # We will let him choose to remove one of them.

                    return Response(status=status.HTTP_400_BAD_REQUEST)

                else:
                    # We can add the client device to the user devices.
                    # See the networking functions in the receivers in portal/models.py

                    dev = Device(user=request.user, ip=client_ip)
                    dev.save()

                # TODO: What shall we do if an user attempts to connect with a device that has the same IP
                # that another device already registered (ie in the Device array) but from a different user account ?
                # We could either kick out the already registered user from the network or refuse the connection of
                # the device that attempts to connect.
        

            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            dev = Device(user=request.user, ip='127.0.0.1')
            dev.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

class DeviceList(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceChangeMark(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, ident, mark):

        if Device.objects.filter(id=ident).count() > 0:
            dev = Device.objects.get(id=ident)
            
            if settings.ENABLE_NETCONTROL:
                r = netcontrol.query("set_mark", {"mac": dev.mac, "mark": mark})

                if r["success"]:
                    return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)


        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

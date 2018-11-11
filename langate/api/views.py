from django.core.exceptions import PermissionDenied

from .serializers import DeviceSerializer
from portal.models import Device
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

# Create your views here.


class UserDeviceListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        qs = Device.objects.filter(user=request.user)
        sz = DeviceSerializer(qs, many=True)
        return Response(sz.data)


class UserDeviceView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_device(self, ident, user):

        # FIXME: This can raise Device.DoesNotExist exception, not sure whether we should catch this...
        dev = Device.objects.get(id=ident)

        # If the API call is made by the device owner or an admin, we should proceed, otherwise we should abort
        if (dev.user == user) or user.is_staff():
            return dev

        else:
                raise PermissionDenied

    def put(self, request, ident, format=None):
        dev = self.get_device(ident, request.user)

        serializer = DeviceSerializer(dev, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ident, format=None):

        dev = self.get_device(ident, request.user)
        dev.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
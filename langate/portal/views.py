from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings

from .models import Device
from modules import network

# Create your views here.


@staff_member_required
def management(request):
    
    context = {"page_name": "management" }

    return render(request, 'portal/management.html', context)


@login_required
def connected(request):

    user_devices = Device.objects.filter(user=request.user)
    client_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    client_mac = network.get_mac(client_ip)

    context = {"page_name": "connected", "too_many_devices": False, "current_ip": client_ip, "widgets": settings.WIDGETS}

    # Checking if the device accessing the gate is already in user devices

    if not user_devices.filter(ip=client_ip).exists():

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

        elif len(user_devices) > 2:
            # If user has too much devices already registered, then we can't connect the device to the internet.
            # We will let him choose to remove one of them.

            context["too_many_devices"] = True

        else:
            # We can add the client device to the user devices.
            # See the networking functions in the receivers in portal/models.py

            dev = Device(user=request.user, ip=client_ip)
            dev.save()
    
    # TODO: What shall we do if an user attempts to connect with a device that has the same IP 
    # that another device already registered (ie in the Device array) but from a different user account ?
    # We could either kick out the already registered user from the network or refuse the connection of
    # the device that attempts to connect.

    return render(request, 'portal/connected.html', context)


@login_required
def disconnect(request):
    
    user_devices = Device.objects.filter(user=request.user)
    client_ip = request.META.get('HTTP_X_FORWARDED_FOR')

    if user_devices.filter(ip=client_ip).exists():
        # When the user decides to disconnect from the portal from a device,
        # we remove the Device from the array (if it still exists) and then we log the user out.

        user_devices.filter(ip=client_ip).delete()
        logout(request)
    
    return redirect(settings.LOGIN_URL)


def faq(request):
    
    context = {"page_name": "faq", "widgets": settings.WIDGETS}
    
    return render(request, 'portal/faq.html', context)


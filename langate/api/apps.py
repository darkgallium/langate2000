from django.apps import AppConfig
from modules import netcontrol
import sys
from django.conf import settings


class LangateConfig(AppConfig):
    name = 'api'

    def ready(self):
        from .models import WhiteListDevice, Device

        # the HACK below is brought to you by
        # https://stackoverflow.com/questions/6791911/execute-code-when-django-starts-once-only

        if not any(x in sys.argv for x in ['makemigrations', 'migrate', 'shell', 'createsuperuser', 'flush', 'collectstatic']) and settings.ENABLE_NETCONTROL:
            print("[PortalConfig] Adding whitelisted devices to the ipset")

            # Connecting whitelisted devices

            for dev in WhiteListDevice.objects.all():
                connect_res = netcontrol.query("connect_user", {"mac": dev.mac, "name": dev.name})
                if not connect_res["success"]:
                    print("[PortalConfig] Could not connect device {}".format(dev.name))

                mark_res = netcontrol.query("set_mark", {"mac": dev.mac, "mark": 0})
                if not mark_res["success"]:
                    print("[PortalConfig] Could not set mark 0 for device {}".format(dev.name))

            # Reconnecting devices registered in the Device set but not in the Ipset
            # This is important when for example the Ipset is flushed, you want the users that are already
            # registered on the gate to be automatically reconnected when the gate restarts.
            # This is important to maintain the consistency between the device state from django's point of view and
            # and the device state from the Ipset's point of view.

            print("[PortalConfig] Adding previously connected devices to the ipset")

            for dev in Device.objects.all():
                connect_res = netcontrol.query("connect_user", {"mac": dev.mac, "name": dev.name})
                if not connect_res["success"]:
                    print("[PortalConfig] Could not connect device {} owned by user {}".format(dev.mac, dev.user.username))


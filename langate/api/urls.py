"""portal app URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

from .views.user import *
from .views.device import *

from rest_framework.authtoken import views

# CRUDs
# - /api/device
# - /api/user
# - /api/whitelist-device
# - /api/announce

# - GET /api/device/self
# - GET /api/user/self
# - GET /api/device/self/connect

# - /api/auth/

# - GET /api/user/<id>/devices
# - PUT /api/device/<id>/mark/<new_mark>

# TODO: markdown preview


urlpatterns = [
    path('device/', DeviceList.as_view()),
    path('device/<int:pk>/', DeviceDetails.as_view()),
    path('device/<int:ident>/mark/<int:mark>', DeviceChangeMark.as_view()),
    path('device/connect', DeviceConnect.as_view()),

    path('user/<int:pk>/devices', UserDeviceList.as_view()),
    path('user/', UserList.as_view()),
    path('user/<int:pk>', AdminUserDetails.as_view()),

    #path('announce/', AnnounceList.as_view()),
    #path('announce/<int:pk>', AnnounceDetails.as_view()),

    #path('whitelist_device/', WhitelistList.as_view()),
    #path('whitelist_device/<int:pk>', WhitelistDetails.as_view()),
    path('auth/user/', UserDetails.as_view()),
    path('auth/', include('dj_rest_auth.urls'))
    #path('markdown_preview/', MarkdownPreview.as_view()),
]

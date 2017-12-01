"""warsztaty3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rezerwacje.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', main),
    url(r'^room/(?P<id>(\d)+$)', room_details),
    url(r'^room/new$', new_room),
    url(r'^modify/(?P<id>(\d)+$)', modify_room),
    url(r'^room/modify/(?P<id>(\d)+$)', add_reservation),
    url(r'^room/delete/(?P<id>(\d)+$)', delete_room),
]

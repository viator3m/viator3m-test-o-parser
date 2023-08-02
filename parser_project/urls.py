from django.contrib import admin
from django.urls import path

from api.v1.views.parser import smoke

urlpatterns = [
    path('smoke/', smoke),
    path('admin/', admin.site.urls),
]

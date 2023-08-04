from django.urls import include, path

from api.v1 import urls as api_v1

urlpatterns = [
    path('v1/', include(api_v1)),
]

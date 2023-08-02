from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.v1.views.parser import ProductDetailView, ProductListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='products-detail') # noqa
]


schema_view = get_schema_view(
   openapi.Info(
      title="Parser API",
      default_version='v1',
      description="Examples requests for Parser API",
      contact=openapi.Contact(email="job@kamyshanov.ru",
                              name="Vladimir Kamyshanov",
                              ),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui')
]

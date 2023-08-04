from celery.result import AsyncResult
from django.conf import settings as conf
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from api.v1.serializers.parser import ProductSerializer, \
    ProductCreateSerializer
from parser.models import Parsing, Product
from parser.utils import parsing


class ProductListView(ListCreateAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        match self.request.method:
            case 'POST': return ProductCreateSerializer
            case _: return ProductSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Successful request",
                examples={"application/json": {"info": "Parsing started"}}
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            products_count = serializer.validated_data.get(
                'products_count', 10
            )
            tasks = parsing.delay(products_count)

            while True:
                task_status = AsyncResult(tasks.task_id).status
                match task_status:
                    case 'PENDING':
                        continue
                    case 'STARTED':
                        return Response(
                            {'info': 'Parsing started'},
                            status=status.HTTP_200_OK
                        )
                    case 'FAILURE':
                        return Response(
                            {'info': 'Something went wrong'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
        return Response(
            {'info': 'Something went wrong'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, *args, **kwargs):
        last_parsing = Parsing.objects.last()
        items = Product.objects.filter(parser=last_parsing)
        serializer = self.get_serializer(data=items, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

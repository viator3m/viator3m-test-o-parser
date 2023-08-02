from celery.result import AsyncResult
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from api.v1.serializers.parser import ProductSerializer
from parser.models import Parsing, Product
from parser.utils import parsing


class ProductListView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        amount = request.data.get('amount', 10)
        if not isinstance(amount, int):
            raise ValidationError({
                'error': f'Amount must be an integer,'
                         f' not {amount.__class__.__name__}'
            })
        tasks = parsing.delay(amount)

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

    def get(self, request, *args, **kwargs):
        last_parsing = Parsing.objects.last()
        items = Product.objects.filter(parser=last_parsing)
        serializer = self.get_serializer(data=items, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

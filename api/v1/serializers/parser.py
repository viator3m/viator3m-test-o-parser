from rest_framework import serializers

from parser.models import Product


class ProductCreateSerializer(serializers.Serializer):
    products_count = serializers.IntegerField(
        min_value=1,
        max_value=50,
        default=10,
        required=False,
    )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'price',
            'link',
            'parser'
        )

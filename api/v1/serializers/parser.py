from rest_framework import serializers

from parser.models import Product


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

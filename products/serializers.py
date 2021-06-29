from rest_framework import serializers
from products.models import Product, ProductView


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "image",
            "sale_price",
            "product_price",
            "created",
            "updated",
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

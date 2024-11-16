from rest_framework import serializers
from .models import Product, Supplier, Category

class ProductSerializer(serializers.ModelSerializer):
    supplier = serializers.CharField(source='supplier.fantasy_name')
    category = serializers.CharField(source='category.name', allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity', 'image_link', 'supplier', 'category']


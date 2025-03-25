import datetime
from rest_framework import serializers
from .models import Order
from shop.models import Product
from shop.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, required=True)
    fullName = serializers.StringRelatedField()
    email = serializers.StringRelatedField()
    phone = serializers.StringRelatedField()
    createdAt = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'createdAt', 'fullName', 'email',
                  'phone', 'deliveryType', 'paymentType',
                  'totalCost', 'status', 'city', 'address',
                  'products',
                  ]

    def get_createdAt(self, instance):
        date = instance.createdAt + datetime.timedelta(hours=3)
        return datetime.datetime.strftime(date, '%d.%m.%Y %H:%M')
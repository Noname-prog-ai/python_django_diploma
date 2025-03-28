from rest_framework import serializers
from app_order.models import Order, Payment
from app_shop.models import Product
from app_shop.serializers import ImageStringField, TagsStringField


class BasketSerializer(serializers.ModelSerializer):
    images = ImageStringField(many=True, read_only=True)
    tags = TagsStringField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        ]


class BasketUpdateSerializer(serializers.Serializer):
    id = serializers.CharField()
    count = serializers.IntegerField()


class OrderSerializer(serializers.ModelSerializer):
    products = BasketSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'number',
            'name',
            'month',
            'year',
            'code',
        ]


class UpdateOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
        ]


# class TagStringField(serializers.StringRelatedField):
#     def to_representation(self, value):
#         return {
#             "id": value.pk,
#             "name": str(value.name)
#         }
#
#
# class ImagesStringField(serializers.StringRelatedField):
#     def to_representation(self, value):
#         return {
#             "src": str(value.src.url),
#             "alt": str(value.pk)
#         }
#
#
# class OrderProductSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(source="product.id")
#     # category = serializers.CharField(source="product.category")
#     category = serializers.PrimaryKeyRelatedField(read_only=True, source="product.category")
#     price = serializers.DecimalField(max_digits=12, decimal_places=2, source="product.price")
#     title = serializers.CharField(source="product.title")
#     count = serializers.IntegerField()
#     date = serializers.DateTimeField(source="product.date")
#     description = serializers.CharField(source="product.description")
#     freeDelivery = serializers.BooleanField(source="product.freeDelivery")
#     images = ImagesStringField(many=True, source="product.images")
#     tags = TagStringField(many=True, source="product.tags")
#     reviews = serializers.IntegerField(source="product.reviews")
#     rating = serializers.DecimalField(max_digits=12, decimal_places=2, source="product.rating")
#
#     class Meta:
#         model = Order
#         fields = [
#                 'id',
#                 'category',
#                 'price',
#                 'count',
#                 'date',
#                 'title',
#                 'description',
#                 'freeDelivery',
#                 'images',
#                 'tags',
#                 'reviews',
#                 'rating',
#             ]
#
#
# class OrderSerializer(serializers.ModelSerializer):
#     fullName = serializers.CharField(source="user.fullName")
#     email = serializers.EmailField(source="user.email")
#     phone = serializers.CharField(source="user.phone")
#     products = OrderProductSerializer(many=True)
#     paymentType = serializers.SlugField()
#
#     class Meta:
#         model = Order
#         fields = [
#             'id',
#             'createdAt',
#             'fullName',
#             'email',
#             'phone',
#             'deliveryType',
#             'paymentType',
#             'totalCost',
#             'status',
#             'city',
#             'address',
#             'products',
#         ]

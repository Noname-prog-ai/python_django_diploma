import datetime
from rest_framework import serializers
from rest_framework import pagination
from .models import (
    Product,
    ProductSpecification,
    Review,
    Tag,
    Sale,
    ProductImage,
)


class ReviewSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()


    class Meta:
        model = Review
        fields = ('author', 'email', 'text', 'rate', 'date')

    def get_date(self, instance):
        date = instance.date + datetime.timedelta(hours=3)
        return datetime.datetime.strftime(date, '%d.%m.%Y %H:%M')

# class ReviewSerializer(serializers.ModelSerializer):
#     reviews = serializers.SerializerMethodField()

#     def get_reviews(self, instance):
#         reviews_count = Review.objects.count()
#         return {"reviews": reviews_count}
    
#     class Meta:
#         model = Review
#         fields = ['reviews'] 

class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ['name', 'value']


class TagsProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()
    alt = serializers.CharField(default='pictures')

    class Meta:
        model = ProductImage
        fields = 'src', 'alt'

    def get_src(self, obj):
        if obj.image:
            return obj.image.url
        return None

class LimitedProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    tags = TagsProductSerializer(many=True, required=False)
    price = serializers.SerializerMethodField()
    

    def get_price(self, instance):
        salePrice = instance.sales.first()
        if salePrice:
            instance.price = salePrice.salePrice
            instance.save()
            return salePrice.salePrice
        return instance.price
    
    def get_reviews(self, obj):
        reviews_count = Review.objects.count()
        return reviews_count
    
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'price', 'count', 'date',
                    'title', 'description',
                    'freeDelivery', 'images', 'tags', 'reviews', 'rating'
                ]


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    reviews = ReviewSerializer(many=True, required=False)
    tags = TagsProductSerializer(many=True, required=False)
    specifications = ProductSpecificationSerializer(many=True, required=False)
    price = serializers.SerializerMethodField()
    

    def get_price(self, instance):
        salePrice = instance.sales.first()
        if salePrice:
            instance.price = salePrice.salePrice
            instance.save()
            return salePrice.salePrice
        return instance.price
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'price', 'count', 'date',
                    'title', 'description', 'fullDescription',
                    'freeDelivery', 'images', 'tags', 'reviews',
                    'specifications', 'rating'
                ]


class SaleSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    title = serializers.StringRelatedField()
    href = serializers.StringRelatedField()
    price = serializers.StringRelatedField()
    dateFrom = serializers.DateField(format='%d.%b')
    dateTo = serializers.DateField(format='%d.%b')
    
    class Meta:
        model = Sale
        fields = '__all__'


class ProductCatalogSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    tags = TagsProductSerializer(many=True, required=False)
    price = serializers.SerializerMethodField()

    def get_price(self, instance):
        salePrice = instance.sales.first()
        if salePrice:
            instance.price = salePrice.salePrice
            instance.save()
            return salePrice.salePrice
        return instance.price
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'price', 'count', 'date',
                    'title', 'description', 'fullDescription',
                    'freeDelivery', 'images', 'tags', 'reviews',
                    'rating',
                ]
    
    def get_reviews(self, obj):
        reviews_count = Review.objects.count()
        return reviews_count
    

class PaginatedProductSerializer(pagination.PageNumberPagination):
    class Meta:
        object_serializer_class = ProductCatalogSerializer
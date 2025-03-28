from decimal import Decimal
from rest_framework import serializers
from shop.models import Product, Review
from shop.serializers import ImageSerializer, TagsProductSerializer


class BascketSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    # images = serializers.SerializerMethodField()
    tags = TagsProductSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    images = ImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id', 'category', 'price', 'count',
                  'date', 'title', 'description',
                  'freeDelivery', 'images',
                  'tags', 'reviews', 'rating',
                  ]

    def get_count(self, obj):
        return self.context.get(str(obj.pk)).get('count')
    
    def get_price(self, obj):
        return Decimal(self.context.get(str(obj.pk)).get('price'))
    
    def get_reviews(self, obj):
        reviews_count = Review.objects.count()
        return reviews_count
    
    

    
    
    # def get_images(self, instance):
    #     images = []
    #     images_tmp = instance.images.all()
    #     for image in images_tmp:
    #         images.append({'src': f'/media{image.__str__()}',
    #                        'alt': image.name})
    #     return images

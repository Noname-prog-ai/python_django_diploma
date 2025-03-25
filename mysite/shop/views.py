from django.db.models import Count
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated

from datetime import datetime

from .models import Product, Sale, Review, Tag
from .serializers import(
    ProductSerializer,
    SaleSerializer,
    TagsProductSerializer,
    ReviewSerializer,
    LimitedProductSerializer,
)



class ProductDetail(APIView):
    def get(self, request: Request, pk):
        product = Product.objects.get(pk=pk)
        print(product)
        serialized = ProductSerializer(product, many=False)
        return Response(serialized.data)
    

class SalesList(APIView):
    def get(self, request: Request):
        sales = Sale.objects.all()
        serialized = SaleSerializer(sales, many=True)
        return Response({'items': serialized.data})
    

class TagsList(APIView):
    def get(self, request: Request):
        tags = Tag.objects.all()
        serialized = TagsProductSerializer(tags, many=True)
        return Response(serialized.data)
    

class LimitedList(APIView):
    def get(self, request: Request):
        products = Product.objects.filter(limited=True)
        serialized = LimitedProductSerializer(products, many=True)
        return Response(serialized.data)
    
class PopularList(APIView):
    def get(self, request: Request):
        products = Product.objects.filter(
            active=True
            ).annotate(count_reviews=Count('reviews')
                       ).order_by('-count_reviews')[:8]
        serialized = LimitedProductSerializer(products, many=True)
        print(products)
        return Response(serialized.data)
    

class CreateReview(CreateModelMixin, GenericAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, pk):
        product = Product.objects.get(pk=pk)
        request.data['date'] = datetime.now()
        request.data['product'] = product.pk
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Review.objects.create(
            author=request.data['author'],
            email=request.data['email'],
            text=request.data['text'],
            rate=request.data['rate'],
            date=datetime.now(),
            product_id=product.pk,
        )

        reviews= Review.objects.filter(product_id=product.pk)
        summa = sum([obj.rate for obj in reviews])
        product.rating = summa / len(reviews)
        product.save()

        return Response(request.data)

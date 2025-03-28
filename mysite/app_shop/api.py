from math import ceil
from django.core.paginator import Paginator
from django.db.models import Count
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from app_shop.models import Category, Product, Tag, Review, Sales
from app_shop.serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductFullSerializer,
    TagSerializer,
    ReviewSerializer,
    SalesSerializer,
    CatalogSerializer,
)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductFullListView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductFullSerializer


class ReviewCreateView(APIView):
    def get(self, request, pk):
        review = Review.objects.filter(product_id=pk)
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        review = Review.objects.create(
            product_id=pk,
            author=request.data["author"],
            email=request.data["email"],
            text=request.data["text"],
            rate=request.data["rate"],
        )
        review.save()

        reviews = Review.objects.filter(product_id=pk)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# class CustomPagination(pagination.PageNumberPagination):
#     page_size = 3
#     page_size_query_param = "page_size"
#     max_page_size = 10
#
#     def get_paginated_response(self, data):
#         return Response(
#             {
#                 'items': data,
#                 "currentPage": self.page.number,
#                 "lastPage": self.page.paginator.num_pages,
#             }
#         )
#
#
# class SalesListView(generics.ListCreateAPIView):
#     queryset = Sales.objects.all()
#     serializer_class = SalesSerializer
#     pagination_class = CustomPagination


class SalesListView(APIView):
    def get(self, data):
        queryset = Sales.objects.all()

        page_number = int(self.request.query_params.get("currentPage"))
        page_size = 3
        paginator = Paginator(queryset, page_size)
        serializer = SalesSerializer(paginator.page(page_number), many=True)

        serializer = {
            "items": serializer.data,
            "currentPage": page_number,
            "lastPage": ceil(len(queryset) / page_size),
        }
        return Response(serializer)


class CatalogListView(APIView):
    def get_queryset(self):
        category = self.request.META['HTTP_REFERER'].split('/')[4]

        if category.isdigit():
            queryset = Product.objects.filter(category_id=category)
        else:
            queryset = Product.objects.all()

        if self.request.query_params:
            name = self.request.query_params.get('filter[name]')
            if name:
                queryset = queryset.filter(title__icontains=name)

            min_price = self.request.query_params.get('filter[minPrice]')
            if min_price:
                queryset = queryset.filter(price__gte=min_price)

            max_price = self.request.query_params.get('filter[maxPrice]')
            if max_price:
                queryset = queryset.filter(price__lte=max_price)

            free_delivery = self.request.query_params.get('filter[freeDelivery]')
            if free_delivery == 'true':
                queryset = queryset.filter(freeDelivery=True)

            available = self.request.query_params.get('filter[available]')
            if available and available == 'true':
                queryset = queryset.filter(count__gte=1)

            sort_param = self.request.query_params.get("sort")
            sort_type = self.request.query_params.get("sortType")

            if sort_param == 'reviews':
                queryset = queryset.annotate(cnt=Count("reviews"))

            if sort_type == 'dec':
                queryset = queryset.order_by(f"-{sort_param}")
            else:
                queryset = queryset.order_by(sort_param)

            tags = dict(self.request.query_params).get('tags[]')
            if tags:
                prod_id = Tag.objects.filter(id__in=tags).values_list('product_id')
                queryset = queryset.filter(id__in=prod_id)
            return queryset

    def get(self, data):
        filtered_products = self.get_queryset()

        page_number = int(self.request.query_params.get("currentPage"))
        # page_size = 3
        page_size = int(self.request.query_params.get("limit"))
        paginator = Paginator(filtered_products, page_size)

        serializer = CatalogSerializer(paginator.page(page_number), many=True)

        serializer = {
            "items": serializer.data,
            "currentPage": page_number,
            "lastPage": ceil(len(filtered_products) / page_size)
        }
        return Response(serializer)

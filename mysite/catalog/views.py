from django.db.models import Count
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import pagination

from .models import Category
from .serializers import CategorySerializer

from shop.models import Product
from shop.serializers import ProductSerializer, ProductCatalogSerializer


class CustomPagination(pagination.PageNumberPagination):
    page_size = 1
    page_query_param = 'page'
    page_size_query_param = 'per_page'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'items': data,
            'current_page': self.page.number,
            'last_page': self.page.paginator.num_pages,
        })

def sort_products(request: Request, products):
    sort = request.GET.get('sort')
    sortType = request.GET.get('sortType')
    if sortType == 'inc':
        sortType = '-'
    else:
        sortType = ''

    if sort == 'reviews':
        products = products.filter(
            active=True
            ).annotate(count_reviews=Count('reviews')
                       ).order_by(
                           f'{sortType}count_reviews'
                           ).prefetch_related('images',
                                              'reviews')
    else:
        products = products.filter(
            active=True
        ).order_by(f'{sortType}{sort}'
                   ).prefetch_related('images',
                                      'reviews')
    return products


def filter_catalog(request:Request):

    title = request.query_params.get('filter[name]')
    available = request.query_params.get('filter[available]')
    freeDelivery = request.query_params.get('filter[freeDelivery]')
    tags = request.query_params.getlist('tags[]')
    min_price = (request.query_params.get('filter[minPrice]'))
    max_price = (request.query_params.get('filter[maxPrice]'))
    category=request.META.get('HTTP_REFERER', '').split('/')
    print(category)
    
    catalog = Product.objects
    
    if category:
        try:
            categories = [obj.pk for obj in Category.objects.filter(parent_id=category)]
            categories.append(int(category))
            print(categories)
            catalog = catalog.filter(category_id__in=categories)
        except:
            if str(category).startswith('?filter='):
                if not title:
                    title = str(category).split('=')[1]
            else:
                category = ''
    
    print(tags)
    if available == 'true':
        if freeDelivery == 'true':
            if len(tags) != 0:
                catalog = (catalog.filter(
                        title__iregex=title, price__range=(min_price, max_price), count__gt=0, freeDelivery=True,
                        tags__in=tags).prefetch_related('images', 'tags')).distinct()
            else:
                catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price), count__gt=0,
                                         freeDelivery=True).prefetch_related('images')
        elif len(tags) != 0:
            catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price), count__gt=0,
                                     tags__in=tags).prefetch_related('images', 'tags').distinct()
        else:
            catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price),
                                     count__gt=0).prefetch_related('images')
    elif freeDelivery == 'true':
        if len(tags) != 0:
            catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price), freeDelivery=True,
                                     tags__in=tags).prefetch_related('images', 'tags').distinct() 
        else:
            catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price),
                                     freeDelivery=True).prefetch_related('images')
    elif len(tags) != 0:
        catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price),
                                 tags__in=tags).prefetch_related('images', 'tags').distinct()
    else:
        catalog = catalog.filter(title__iregex=title, price__range=(min_price, max_price)).prefetch_related('images')
    
    return catalog
    

# class Catalog(APIView):
#     def get(self, request: Request):
#         products = filter_catalog(request)
#         products = sort_products(request, products)
#         serialized = ProductCatalogSerializer(products, many=True)
#         return Response({'items': serialized.data})
    

class Catalog(APIView):
    def get(self, request: Request):
        products = filter_catalog(request)
        products = sort_products(request, products)
        
        paginator = CustomPagination()
        if 'currentPage' in request.query_params and request.query_params['currentPage'] is not None:
            paginated_products = paginator.paginate_queryset(products, request)
        else:
            paginated_products = products
        
        serialized = ProductCatalogSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serialized.data)


class BannerList(APIView):
    def get(self, request: Request):
        fav_categories = [obj.pk for obj in Category.objects.filter(favorite=True)]
        banners = Product.objects.filter(
            category_id__in=fav_categories
        )
        serialized = ProductSerializer(banners, many=True)
        return Response(serialized.data)
    

class CategoriesList(APIView):
    def get(self, request: Request):
        categories = Category.objects.filter(parent=None)
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data)
    

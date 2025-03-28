from django.urls import path
from app_shop.api import (
    CategoryListView,
    ProductListView,
    ProductFullListView,
    TagListView,
    SalesListView,
    CatalogListView,
    ReviewCreateView,
)

app_name = "app_shop"

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('banners/', ProductListView.as_view(), name='banners'),
    path('products/popular/', ProductListView.as_view(), name='products_popular'),
    path('products/limited/', ProductListView.as_view(), name='products_limited'),
    path('product/<int:pk>/', ProductFullListView.as_view(), name='product'),
    path('product/<int:pk>/review/', ReviewCreateView.as_view(), name='product_review'),
    path('product/<int:pk>/reviews', ReviewCreateView.as_view(), name='product_update_review'),
    path('tags/', TagListView.as_view(), name='tags'),
    path('sales/', SalesListView.as_view(), name='sales'),
    path('catalog/', CatalogListView.as_view(), name='catalog'),
]


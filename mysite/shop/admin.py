from django.contrib import admin
from .models import (
    Product,
    ProductImage,
    ProductSpecification,
    Tag,
    Review,
    Sale,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'category', 'price', 'active']
    list_display_links = ['pk', 'title']
    oredering = ['pk', '-date']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'product']
    list_display_links = ['pk', 'name']
    ordering = ['pk',]


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'value', 'product']
    list_display_links = ['pk', 'name']
    ordering = ['pk',]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display= ['pk', 'author', 'date', 'product']
    list_display_links = ['pk', 'product']
    ordering = ['pk',]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    list_display_links = ['pk',]
    ordering = ['pk',]


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'salePrice']
    list_display_links = ['pk', 'title']
    ordering = ['pk',]

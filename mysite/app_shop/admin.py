from django.contrib import admin
from app_shop.models import (
    Category,
    Product,
    Shop,
    Subcategories,
    Review,
    Specification,
    Tag,
    ImageProduct,
    Sales,
)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'created_by',
        'date_creation',
    ]
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
    ]
    list_display_links = ['title']
    search_fields = ['title']
    list_filter = ['title']


@admin.register(Subcategories)
class SubcategoriesAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'category',
    ]
    list_display_links = ['title']
    search_fields = ['title']
    list_filter = ['title']


class ReviewTabularInline(admin.TabularInline):
    model = Review
    extra = 0


class ImageProductTabularInline(admin.TabularInline):
    model = ImageProduct


class SpecificationTabularInline(admin.TabularInline):
    model = Specification


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'product',
    ]
    list_display_links = ['id']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'category',
        'price',
        'count',
        'date',
        'description',
        'fullDescription',
        'freeDelivery',
        'reviews',
        'rating',
        'sold_amount',
        'shop',
    ]
    list_display_links = ['title']
    inlines = [
            ImageProductTabularInline,
            SpecificationTabularInline,
            ReviewTabularInline,
        ]


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'price',
        'salePrice',
        'dateFrom',
        'dateTo',
    ]
    list_display_links = ['title']
    inlines = [
        ImageProductTabularInline,
    ]

# @admin.register(ImageProduct)
# class ProductImagesAdmin(admin.ModelAdmin):
#     list_display = [
#         field.name for field in ImageProduct._meta.get_fields()
#     ]


# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'author',
#         'email',
#         'text',
#         'rate',
#         'date',
#         'user',
#     ]
#     list_display_links = ['id']
#     search_fields = ['author', 'text']
#     list_filter = ['rate']


# @admin.register(Specification)
# class SpecificationAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'name',
#         'value',
#         'product',
#     ]
#     list_display_links = ['id']
#     search_fields = ['name']

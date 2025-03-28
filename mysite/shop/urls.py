from django.urls import path
from .views import(
    ProductDetail,
    PopularList,
    LimitedList,
    SalesList,
    CreateReview,
    TagsList,
)


urlpatterns = [
    path('api/product/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('api/product/<int:pk>/reviews', CreateReview.as_view(), name='product_reviews'),
    path('api/tags', TagsList.as_view(), name='tags_list'),
    path('api/products/popular', PopularList.as_view(), name='products_popular'),
    path('api/products/limited', LimitedList.as_view(), name='product_limited'),
    path('api/sales', SalesList.as_view(), name='sales'),

]
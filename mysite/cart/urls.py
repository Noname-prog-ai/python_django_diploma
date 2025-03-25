from django.urls import path
from .views import BascketProductsView

app_name = 'cart'

urlpatterns = [
    path('api/basket', BascketProductsView.as_view(), name='basket'),
    path('api/cart', BascketProductsView.as_view(), name='cart'),
]
from django.urls import path
from .views import Orders, OrderDetail, PaymentView


urlpatterns = [
    path('api/orders', Orders.as_view()),
    path('api/orders/<int:pk>', OrderDetail.as_view()),
    path('api/payment/<int:pk>', PaymentView.as_view()),
]
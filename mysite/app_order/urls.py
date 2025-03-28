from django.urls import path
from app_order.api import PaymentListView, BasketListView, OrdersView, OrderCreateView

app_name = "app_order"


urlpatterns = [
    path("orders", OrderCreateView.as_view(), name="orders_post"),
    path("order/<int:pk>/", OrdersView.as_view(), name="order"),
    path("order/<int:pk>", OrdersView.as_view(), name="order_confirm"),
    path("payment/<int:pk>", PaymentListView.as_view(), name="payment"),
    path("basket", BasketListView.as_view(), name="basket"),
]

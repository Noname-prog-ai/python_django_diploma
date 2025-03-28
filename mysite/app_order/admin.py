from django.contrib import admin
from app_order.models import Order, Payment, Basket


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "createdAt",
        "deliveryType",
        "paymentType",
        "totalCost",
        "status",
        "city",
        "address",
    ]
    list_display_links = ["user"]
    search_fields = ["user"]
    ordering = ["-createdAt"]


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "product",
        "price",
        "count",
    ]
    list_display_links = ["product"]
    search_fields = ["product"]
    ordering = ["id"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "number",
        "name",
        "month",
        "year",
        "code",
    ]
    list_display_links = ["name"]
    search_fields = ["number"]
    ordering = ["-number"]

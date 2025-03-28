from django.db import models
from app_shop.models import Product
from app_auth.models import ProfileUser


class Order(models.Model):
    user = models.ForeignKey(
        ProfileUser,
        on_delete=models.CASCADE,
        related_name="user_order",
        verbose_name="Пользователь",
    )
    createdAt = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    fullName = models.CharField(
        max_length=120,
        verbose_name="ФИО",
        default=None,
        null=True,
    )
    email = models.CharField(
        max_length=50,
        verbose_name="эл.почта",
        default=None,
        null=True,
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="телефон",
        default=None,
        null=True,
    )
    deliveryType = models.CharField(
        max_length=120,
        verbose_name="Доставка",
        default="free",
    )
    paymentType = models.CharField(
        max_length=50,
        verbose_name="Способ оплаты",
        default="online",
        null=True,
    )
    totalCost = models.DecimalField(
        max_digits=12,
        default=0,
        decimal_places=2,
        verbose_name="Общая стоимость",
    )
    status = models.CharField(
        max_length=20,
        default="checkout",
        verbose_name="Статус",
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Город",
        default=None,
        null=True,
    )
    address = models.CharField(
        max_length=120,
        default=None,
        null=True,
        verbose_name="Адрес",
    )
    products = models.ManyToManyField(
        Product,
        related_name="order_product",
        verbose_name="продукты",
    )

    def __str__(self):
        return f"№_{self.id}"

    class Meta:
        ordering = ["-createdAt", "-status"]
        verbose_name = "заказ"
        verbose_name_plural = "заказы"
        db_table = "orders"


class Basket(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="product",
        on_delete=models.PROTECT,
        verbose_name="Продукт",
    )
    price = models.DecimalField(
        max_digits=1000000,
        default=0,
        blank=False,
        decimal_places=2,
        verbose_name="Цена",
    )
    count = models.PositiveIntegerField(
        default=0,
        blank=False,
        verbose_name="Количество",
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def __str__(self):
        return f'Корзина c товаром - {self.product}'

    def get_cost(self):
        return self.price * self.count


class Payment(models.Model):
    user = models.ForeignKey(
        ProfileUser,
        on_delete=models.PROTECT,
        verbose_name="Пользователь",
        default=None,
        null=True,
    )
    number = models.CharField(
        max_length=20,
        verbose_name="Оплата",
        default=None,
        null=True,
    )
    name = models.CharField(
        max_length=20,
        verbose_name="Имя владельца",
        default=None,
        null=True,
    )
    month = models.CharField(
        max_length=20,
        verbose_name="Месяц",
        default=None,
        null=True,
    )
    year = models.CharField(
        max_length=20,
        verbose_name="Год",
        default=None,
        null=True,
    )
    code = models.CharField(
        max_length=20,
        verbose_name="Код",
        default=None,
        null=True
    )

    def __str__(self):
        return f"Оплата {self.number}"

    class Meta:
        verbose_name = 'способ оплаты'
        verbose_name_plural = 'способы оплаты'
        db_table = "payments"

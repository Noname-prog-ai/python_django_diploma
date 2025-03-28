from django.db import models
from shop.models import Product
from myauth.models import Profile


class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,
                             verbose_name='user', related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders',
                                      verbose_name='products')
    address = models.CharField(max_length=200, default='',
                               verbose_name='address')
    city = models.CharField(max_length=200, default='',
                            verbose_name='city')
    deliveryType = models.CharField(max_length=150, default='',
                                    verbose_name='type delivery')
    paymentType = models.CharField(max_length=150, default='',
                                   verbose_name='type payment')
    totalCost = models.DecimalField(max_digits=10, decimal_places=2,
                                    default=0, verbose_name='total cost')
    status = models.CharField(max_length=150, default='',
                              verbose_name='status')
    createdAt = models.DateTimeField(auto_now_add=True,
                                      verbose_name='date creation')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def email(self):
        return self.user.email
    
    def fullName(self):
        return self.user.fullName
    
    def phone(self):
        return self.user.phone
    
    def orderId(self):
        return f'{self.pk}'
    
    def __str__(self) -> str:
        return f'{self.pk}'
    

class CountProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    count = models.PositiveIntegerField()
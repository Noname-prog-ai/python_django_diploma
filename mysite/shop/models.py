from django.db import models
from catalog.models import Category


def product_image_directory_path(instanse: 'ProductImage', filename: str) -> str:
    return 'products/images/{pk}/{filename}'.format(
        pk=instanse.product.pk,
        filename=filename
    )




class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name='products')
    title = models.CharField(max_length=150, null=False, blank=False)
    description = models.CharField(max_length=250, null=False, blank=True)
    fullDescription = models.TextField(null=False, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                null=False)
    count = models.IntegerField(default=0, null=False)
    date = models.DateTimeField(auto_now_add=True, null=False)
    freeDelivery= models.BooleanField(default=True)
    limited = models.BooleanField(default=False)
    rating = models.DecimalField(default=0, max_digits=3, decimal_places=2,
                                 null=False)
    active = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', blank=True, related_name='products')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['pk', '-date']

    def __str__(self) -> str:
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=150, null=False, blank=True)
    
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['pk',]

    def __str__(self) -> str:
        return self.name    
    

class ProductImage(models.Model):
    name = models.CharField(max_length=200, null=False, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images', verbose_name='product')
    image = models.FileField(upload_to=product_image_directory_path)

    class Meta:
        verbose_name = 'Product image'
        verbose_name_plural = 'Product images'
        ordering = ['pk',]

    def src(self):
        return self.image

    def __str__(self) -> str:
        return self.name
    
    
class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='specifications')
    name = models.CharField(max_length=250, default='')
    value = models.CharField(max_length=250, default='')

    class Meta:
        verbose_name = 'Product specifications'
        verbose_name_plural = 'Product specifications'
    

class Review(models.Model):
    author = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    text = models.TextField(default='')
    rate = models.PositiveSmallIntegerField(blank=False, default=5)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='reviews', verbose_name='product')
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['pk',]

    def __str__(self) -> str:
        return f"{self.author}: {self.product.title}"
    

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='sales')
    salePrice = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                    db_index=True)
    dateFrom = models.DateField(default='')
    dateTo = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'

    def price(self):
        return self.product.price
    
    def title(self):
        return self.product.title
    
    def href(self):
        return f'/product/{self.product.pk}'
    
    def __str__(self) -> str:
        return self.product.title
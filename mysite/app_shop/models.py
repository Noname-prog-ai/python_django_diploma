from django.db import models
from app_auth.models import ProfileUser


class Category(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name='категория'
    )
    image = models.ImageField(
        upload_to='image_category/',
        verbose_name='изображение категории',
        blank=True
    )

    class Meta:
        db_table = 'category'
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['title']

    def __str__(self):
        return self.title


class Subcategories(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name='подкатегория'
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='категория'
    )
    image = models.ImageField(
        upload_to='subcategories/',
        verbose_name='изображение подкатегории',
        blank=True
    )

    class Meta:
        db_table = 'subcategories'
        verbose_name = 'подкатегория'
        verbose_name_plural = 'подкатегории'
        ordering = ['title']

    def __str__(self):
        return self.title


class Shop(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='магазин'
    )
    created_by = models.ForeignKey(
        ProfileUser, on_delete=models.RESTRICT,
        verbose_name='создатель магазина'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )

    class Meta:
        db_table = 'shop'
        verbose_name = 'магазин'
        verbose_name_plural = 'магазины'

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name='название товара'
    )
    category = models.ForeignKey(
        Category,
        related_name='product',
        on_delete=models.PROTECT,
        verbose_name='категория товара'
    )
    price = models.DecimalField(
        max_digits=1000000,
        default=0,
        blank=False,
        decimal_places=2,
        verbose_name='цена'
    )
    count = models.PositiveIntegerField(
        default=0,
        blank=False,
        verbose_name='количество'
    )
    date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name='дата создания'
    )
    description = models.TextField(
        max_length=2000,
        blank=True,
        null=False,
        verbose_name='описание товара'
    )
    fullDescription = models.TextField(
        max_length=3000,
        blank=True,
        verbose_name='полное описание'
    )
    freeDelivery = models.BooleanField(
        default=True,
        verbose_name='категория активна'
    )
    reviews = models.IntegerField(
        default=0,
        blank=False,
        verbose_name='отзыв'
    )
    rating = models.DecimalField(
        max_digits=100,
        default=0,
        blank=False,
        decimal_places=2,
        verbose_name='рейтинг'
    )
    sold_amount = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='количество проданного товара'
    )
    shop = models.ForeignKey(
        Shop,
        null=True,
        on_delete=models.PROTECT,
        verbose_name='магазин'
    )

    class Meta:
        ordering = ['-sold_amount']
        db_table = 'product'
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def __str__(self):
        return f'{self.title} - {self.price} руб.'


class Review(models.Model):
    author = models.CharField(
        verbose_name="Автор",
        max_length=25,
        null=True
    )
    email = models.EmailField(
        max_length=100,
        verbose_name='Email'
    )
    text = models.TextField(
        verbose_name="Содержание",
        max_length=255,
        null=True
    )
    rate = models.FloatField(
        null=True,
        default=0,
        verbose_name="Рейтинг"
    )
    date = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
        null=True
    )
    user = models.ForeignKey(
        ProfileUser,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='review',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.rate}'

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"
        db_table = "comments"


class Tag(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='tags',
        blank=True,
        null=True
    )
    name = models.CharField(
        max_length=32
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "характеристика"
        verbose_name_plural = "характеристики"
        db_table = "specification_names"


class Specification(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='specifications',
        blank=True,
        null=True
    )
    name = models.CharField(
        max_length=32,
        null=False,
        verbose_name="Название",
    )
    value = models.CharField(
        max_length=32,
        null=False,
        verbose_name="Значение",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "спецификация"
        verbose_name_plural = "спецификации"
        db_table = "specifications"


class ImageProduct(models.Model):
    src = models.ImageField(
        upload_to='image_category/',
        verbose_name='изображение'
    )
    alt = models.CharField(
        max_length=100,
        default='string'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='images',
        blank=True, null=True
    )
    sales = models.ForeignKey(
        'Sales',
        on_delete=models.PROTECT,
        related_name='images',
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.product}"

    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продуктов"


class Sales(models.Model):
    price = models.DecimalField(
        max_digits=1000000,
        default=0,
        blank=False,
        decimal_places=2,
        verbose_name='цена'
    )
    salePrice = models.DecimalField(
        max_digits=1000000,
        default=0,
        blank=False,
        decimal_places=2,
        verbose_name='цена продажи'
    )
    dateFrom = models.DateField(
        blank=True,
        null=True,
        verbose_name='дата создания'
    )
    dateTo = models.DateField(
        blank=True,
        null=True,
        verbose_name='дата окончания'
    )
    title = models.CharField(
        max_length=128,
        verbose_name='название'
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT,
        related_name='sales'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'акция'
        verbose_name_plural = 'акции'

    def __str__(self):
        return f'{self.product}'

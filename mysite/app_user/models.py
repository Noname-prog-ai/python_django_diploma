# from django.contrib.auth.models import User
# from django.db import models
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(
#         User,
#         related_name='profile',
#         on_delete=models.CASCADE,
#         verbose_name='Пользователь'
#     )
#     fullName = models.CharField(
#         max_length=100,
#         verbose_name='Имя'
#     )
#     email = models.EmailField(
#         max_length=100,
#         verbose_name='Email'
#     )
#     phone = models.CharField(
#         max_length=11,
#         unique=True,
#         verbose_name='Номер телефона'
#     )
#     avatar = models.ImageField(
#         verbose_name='Изображение профиля',
#         upload_to='alt/profile/',
#         null=True,
#         blank=True
#     )
#
#     class Meta:
#         verbose_name = 'Профиль'
#         verbose_name_plural = 'Профили'
#
#     def __str__(self):
#         return self.user.username

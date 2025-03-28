from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator


class ProfileUser(AbstractUser):
    image_validator = FileExtensionValidator(
        allowed_extensions=['png', 'jpg', 'svg'],
        message='Расширение файла может быть только png, jpg или svg'
    )
    phone_number_validator = RegexValidator(
        regex=r"^\d{10}$"
    )

    def size_file_validator(file):
        file_size = file.file.size
        mb_limit = 2.0
        if file_size > mb_limit * 1024 * 1024:
            raise ValidationError(f"Максимальный размер файла {mb_limit}MB", code='invalid')

    fullName = models.CharField(
        max_length=100,
        verbose_name='ФИО'
    )
    phone = models.CharField(
        max_length=10,
        validators=[phone_number_validator],
        verbose_name='Телефон',
        null=True,
        blank=True,
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        null=True,
        blank=True,
        validators=[image_validator, size_file_validator],
        verbose_name='Аватар'
    )
    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.fullName

    REQUIRED_FIELDS = ['fullName', 'password']

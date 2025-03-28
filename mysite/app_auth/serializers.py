from rest_framework import serializers
from app_auth.models import ProfileUser


class ChangeInfoSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(
        max_length=100,
        required=False
    )
    phone = serializers.CharField(
        max_length=10,
        validators=[ProfileUser.phone_number_validator],
        required=False
    )
    email = serializers.EmailField(
        required=False
    )

    class Meta:
        model = ProfileUser
        fields = ['fullName', 'phone', 'email']


class ChangePasswordSerializer(serializers.ModelSerializer):
    passwordCurrent = serializers.CharField(
        required=True
    )
    password = serializers.CharField(
        required=True
    )
    passwordReply = serializers.CharField(
        required=True
    )

    class Meta:
        model = ProfileUser
        fields = ['passwordCurrent', 'password', 'passwordReply']


class ChangeAvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = ProfileUser
        fields = ['avatar']

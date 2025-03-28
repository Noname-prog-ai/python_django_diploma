# from rest_framework import serializers
# from app_user.models import Profile
#
#
# class CustomField(serializers.Field):
#     def to_representation(self, value):
#         ret = {
#             'src': str(value.url),
#             'alt': str(value.name)
#         }
#         return ret
#
#
# class ProfileSerializer(serializers.ModelSerializer):
#     avatar = CustomField()
#
#     class Meta:
#         model = Profile
#         fields = ['fullName', 'email', 'phone', 'avatar']

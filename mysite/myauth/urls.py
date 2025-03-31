from django.urls import path
from .views import (
    RegistrationView,
    LogoutView,
    LoginView,
    ProfileDetail,
    AvatarUpdatedView,
    ChangePassword)


urlpatterns = [
    path('api/sign-up', RegistrationView.as_view(), name='sign_up'),
    path('api/sign-in', LoginView.as_view(), name='sign_in'),
    path('api/sign-out', LogoutView.as_view(), name='sign_out'),
    path('api/profile', ProfileDetail.as_view(), name='profile_detail'),
    path('api/profile/avatar', AvatarUpdatedView.as_view(), name='profile_avatar'),
    path('api/profile/password', ChangePassword.as_view(), name='profile_password'),    
]

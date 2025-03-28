from django.urls import path
from app_auth import views


app_name = "app_auth"

urlpatterns = [
    path('sign-in', views.signIn),
    path('sign-up', views.signUp),
    path('sign-out', views.signOut),
    path('profile/', views.ProfileGetAndPostView.as_view()),
    path('profile/avatar/', views.ChangeAvatarView.as_view()),
    path('profile/password', views.ChangePasswordView.as_view()),
]

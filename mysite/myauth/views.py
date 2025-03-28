from rest_framework import status
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProfileSerializer, PasswordChangeSerializer
from django.contrib.auth.views import LogoutView
from .models import Profile, Avatar
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
import json


class RegistrationView(APIView):
    def post(self, request: Request):
        data = json.loads(list(request.data.keys())[0])
        serializer = UserSerializer(data=data)
        username = data.get('username')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            name = data.get('name')
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            try:
                user = User.objects.create_user(username=username, password=password)
                user.first_name = name
                user.save()
                Profile.objects.create(user=user, fullName=name)
                user = authenticate(username=username, password=password)
                login(request, user)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'success': 'Registered successfully'}, status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    def post(self, request):
        data = json.loads(list(request.data.keys())[0])
        print(data)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username,
                            password=password)
        if user is not None:
            login(request, user)
        else:
            return Response('Invalid credantials', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response('Authentication successful', status=status.HTTP_200_OK)

        

class LogoutView(LogoutView):
    next_page = reverse_lazy('users:sign-in')


class ProfileDetail(APIView):
    def get(self, request: Request):
        user = request.user.pk
        profile = Profile.objects.get(user_id=user)
        serializer =  ProfileSerializer(profile, many=False)
        return Response(serializer.data)
    
    def post(self, request: Request):
        data = request.data
        user = request.user.pk
        profile = Profile.objects.get(user_id=user)

        profile.fullName = data.get('fullName')
        profile.phone = data.get('phone')
        profile.email = data.get('email')
        profile.save()

        return Response('Update successful', status=status.HTTP_200_OK)
    

class AvatarUpdatedView(APIView):
    def post(self, request: Request):
        new_avatar = request.data.get('avatar')
        user = request.user.pk
        profile = Profile.objects.get(user_id=user)
        avatar, created = Avatar.objects.get_or_create(
            profile_id=profile.pk
        )

        if str(new_avatar).endswith('.jpeg', '.jpg', '.png'):
            avatar.image = new_avatar
            avatar.save()
        else:
            return Response('Wrong file format', status=status.HTTP_400_BAD_REQUEST)
        
        return Response('Updated successful', status=status.HTTP_200_OK)
    

class ChangePassword(GenericAPIView, UpdateModelMixin):
    serializer_class = PasswordChangeSerializer

    def get_object(self):
        return self.request.user
    
    def post(self, *args, **kwargs):
        return self.update(self.request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.date.get('passwordCurrent')):
                return Response({'passwordCurrent': ['Wrong password']},
                                status=status.HTTP_400_BAD_REQUEST)
            
            elif not serializer.data.get('password') == serializer.data.get('passwordReply'):
                return Response({'password': ['Password must match']},
                                status=status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(serializer.data.get(
                'passwordReply'
            ))
            self.object.save()

            return Response('Updated successful',
                            status=status.HTTP_200_OK)
    
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
import json
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from app_auth.models import ProfileUser
from app_auth.serializers import ChangeInfoSerializer, ChangePasswordSerializer, ChangeAvatarSerializer


def signOut(request):
    logout(request)
    return HttpResponse(status=200)


def signIn(request):
    if request.method == "POST":
        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)


def signUp(request):
    if request.method == "POST":
        body = json.loads(request.body)
        name = body["name"]
        username = body["username"]
        password = body["password"]
        customer = ProfileUser(fullName=name, username=username)
        customer.set_password(password)
        customer.save()

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)


class ChangePasswordView(GenericAPIView):
    queryset = ProfileUser.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        profile = ProfileUser.objects.get(pk=request.user.pk)
        request_data = self.serializer_class(data=request.data)

        if request_data.is_valid():
            if not profile.check_password(request_data.data.get('passwordCurrent')):
                return Response(data={'passwordCurrent': 'Неверный пароль'}, status=status.HTTP_400_BAD_REQUEST)
            elif request_data.data.get('password') != request_data.data.get('passwordReply'):
                return Response(data={'password': 'Неверный пароль'}, status=status.HTTP_400_BAD_REQUEST)
            profile.set_password(request_data.data.get('password'))
            profile.save()
            return Response(data={'password': request_data.data.get('password')}, status=status.HTTP_200_OK)
        return Response(data=request_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileGetAndPostView(APIView):
    queryset = ProfileUser.objects.all()
    serializer_class = ChangeInfoSerializer

    def get(self, request):
        profile = ProfileUser.objects.get(pk=request.user.pk)
        if profile.avatar:
            return Response(
                data={
                    'fullName': profile.fullName,
                    'email': profile.email,
                    'phone': profile.phone,
                    'avatar': {
                        'src': profile.avatar.url,
                        'alt': f'avatar_{profile.pk}'
                    }
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={
                    'fullName': profile.fullName,
                    'email': profile.email,
                    'phone': profile.phone,
                },
                status=status.HTTP_200_OK
            )

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            profile = ProfileUser.objects.get(pk=request.user.pk)
            request_data = self.serializer_class(data=request.data)

            if request_data.is_valid():
                profile.fullName = request_data.data.get('fullName')
                profile.phone = request_data.data.get('phone')
                profile.email = request_data.data.get('email')
                profile.save()
                if profile.avatar:
                    return Response(
                        data={
                            'fullName': profile.fullName,
                            'email': profile.email,
                            'phone': profile.phone,
                            'avatar': {
                                'src': profile.avatar.url,
                                'alt': f'avatar_{profile.pk}'
                            }
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        data={
                            'fullName': profile.fullName,
                            'email': profile.email,
                            'phone': profile.phone,
                        },
                        status=status.HTTP_200_OK
                    )
            return Response(data=request_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeAvatarView(APIView):
    queryset = ProfileUser.objects.all()
    serializer_class = ChangeAvatarSerializer

    def post(self, request, *args, **kwargs):
        profile = ProfileUser.objects.get(pk=request.user.pk)
        request_data = self.serializer_class(data=request.data)

        if request_data.is_valid():
            profile.avatar = request_data.validated_data.get('avatar')
            profile.save()
            return Response(status=status.HTTP_200_OK)
        return Response(data=request_data.errors, status=status.HTTP_400_BAD_REQUEST)

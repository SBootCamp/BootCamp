import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import IntegrityError
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import ProfileSerializerView


class RegistrationUserView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ProfileSerializerView

    def get(self, request):
        return Response({"hello": "please fill in the fields below"})

    def post(self, request):
        serializer = ProfileSerializerView(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                if User.objects.get(username=request.data['user.username']):
                    return Response({"message": "пользователь с таким 'username' уже существует"})
            except User.DoesNotExist:
                registration_view(request, request.data)
                return Response({"success": "please wait, your account is verified"})


def registration_view(request, validated_data):
    user_data = dict(validated_data)
    new_link = 'http://127.0.0.1:8000/registration/check/?username=' + user_data['user.username'][0] + '&first_name=' + \
               user_data['user.first_name'][0] + '&last_name=' + user_data['user.last_name'][0] + '&email=' + \
               user_data['user.email'][0] + '&github=' + user_data['github'][0] + '&number_phone=' + \
               user_data['number_phone'][0] + '&password=' + user_data['password'][0]
    send_link(new_link)


def send_link(new_link):
    send_mail(
        'Create new profile',
        str(new_link),
        os.getenv("EMAIL_HOST_USER"),
        ['test@gmail.com'],
    )


class Check(APIView):
    # Note: when mentor click on a link, the browser sends a get request
    def get(self, request):
        username = request.GET.get('username', '')
        first_name = request.GET.get('first_name', '')
        last_name = request.GET.get('last_name', '')
        email = request.GET.get('email', '')
        github = request.GET.get('github', '')
        number_phone = request.GET.get('number_phone', '')
        password = request.GET.get('password', '')

        try:
            user = User(username=username, first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            user.save()
            profile = Profile(user=user, github=github, number_phone=number_phone, password=password)
            profile.save()
            return Response({"success": "Аккаунт создан "})
        except IntegrityError:
            return Response({"message": "Аккаунт уже создан "})


class Login(APIView):
    def get(self, request):
        user = authenticate(username=request.GET.get('username', ''), password=request.GET.get('password', ''))
        if user is not None:
            login(request, user)
            return Response(status=200, data={"token": str(Token.objects.get(user=user))})
        else:
            return Response(status=403, data={"message": "Неправильный ввод данных"})


class Logout(APIView):
    def get(self, request):
        logout(request)
        return Response(status=200, data={"message": "Успешный выход из системы"})

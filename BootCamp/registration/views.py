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

import json
from datetime import datetime

import generics as generics
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, request, status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from .serializers import ScheduleSSerializer, StudentsSerializer, ForPutSerializer, \
    ForPostSerializer, MentorSerializer
from .models import ScheduleS
from django.views import generic

from .models import ScheduleS

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

def table_students(request):
    student_ = Profile.objects.all()
    schedule_ = ScheduleS.objects.all()
    # student_schedule_ = StudentScheduleS.objects.all()
    res = '<h1>Расписание студентов</h1>'

    import datetime

    d1 = datetime.datetime.today()
    d1 = d1 + datetime.timedelta(days=1)
    days_with_st = [i.day_of_week for i in schedule_]
    good_form = [el.strftime("%Y %A %d %B ") for el in days_with_st]

    for i in range(30):
        for elem in good_form:
            d2 = d1 + datetime.timedelta(days=i)
            if elem == d2.strftime("%Y %A %d %B "):
                res += f'<div> {d2.strftime("%Y %A %d %B ")}{[item.name for item in student_ ]}</div>'
            else:
                pass

    return HttpResponse(res)


class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = StudentsSerializer

    def delete(self, id):
        change = Profile.objects.get(id=id)
        change.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # serializer = StudentsSerializer(change, data=request.data)
        # if serializer.is_valid():
        #     change.delete()
        # return Response(status=status.HTTP_200_OK)


class ScheduleAPIView(APIView):

    def get(self, request):
        queryset = Profile.objects.all()
        res = StudentsSerializer(queryset, many=True)
        return Response(data=res.data)


class OneStudentSchedule(APIView):

    def get_queryset(self, *args, **kwargs):
        res = Profile.objects.all()
        return res

    def get_object(self, id):
        return get_object_or_404(self.get_queryset(), id=id)

    def get(self, request, id=None):
        id = id or request.query_params.get('id')
        if id:
            answer = StudentsSerializer(self.get_object(id))
        else:
            answer = StudentsSerializer(self.get_queryset(), many=True)

        return Response(answer.data)

    @staticmethod
    def post(request, id=None):
        try:
            answer = Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            return Response(status=400, data={'error': 'student not found'})
        ser = ForPostSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        for_add = ScheduleS.objects.create(day_of_week=data.get('day_of_week'), pk=data.get('id'))
        for_save = answer.schedule.add(for_add)
        try:
            for_save.save()
        except AttributeError:
            return Response(status=status.HTTP_201_CREATED)
        return Response(for_save.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def put(request: Request, schedule_s_id: int) -> Response:
        # user_id = request.query.get('user_id')
        # user = Student.objects.get(pk=user_id)
        try:
            user_schedule = ScheduleS.objects.get(pk=schedule_s_id)
        except ScheduleS.DoesNotExist:
            return Response(status=400, data={'error': 'schedule not found'})
        ser = ForPutSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        user_schedule.day_of_week = data.get('day_of_week') or user_schedule.day_of_week
        return Response(ScheduleSSerializer(user_schedule).data)

    @staticmethod
    def delete(request: Request, schedule_s_id: int) -> Response:
        try:
            schedule_for_del = get_object_or_404(ScheduleS, pk=schedule_s_id)
            schedule_for_del.delete()
        except ScheduleS.DoesNotExist:
            return Response(schedule_for_del.data)
        return Response(status=status.HTTP_200_OK, data={'deleted': 'schedule was deleted'})

class ScheduleSViewSet(viewsets.ModelViewSet):
    queryset = ScheduleS.objects.all()
    serializer_class = ScheduleSSerializer



from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ScheduleSSerializer, StudentsSerializer, StudentScheduleSSerializer
from .models import Student, ScheduleS, StudentScheduleS
from django.views import generic

from .models import Student, Mentor, ScheduleS


@login_required
def index(request):
    name_st = Student.name
    name_mt = Mentor.name
    email_st = Student.email
    email_mt = Mentor.email
    git = Student.github
    phone = Student.number_phone

    return render(
        request,
        'index.html',
        context={'name_st': name_st, 'name_mt': name_mt,
                 'email_st': email_st, 'email_mt': email_mt,
                 'git': git, 'phone': phone},
    )

def table_students(request):
    some = Student.objects.all()
    some2 = ScheduleS.objects.all()
    res = '<h1>имена</h1>'
    for item in some:
        for i in some2:
            res += f'<div> {item.name} {item.email} {i.day_of_week}</div>'
    return HttpResponse(res)

class StudentsViewSet(viewsets.ModelViewSet):
    # queryset = Student.objects.filter(schedule__day_of_week='monday')
    queryset = Student.objects.all()
    serializer_class = StudentsSerializer

class ScheduleSViewSet(viewsets.ModelViewSet):
    queryset = ScheduleS.objects.all()
    serializer_class = ScheduleSSerializer

class StudentScheduleSViewSet(viewsets.ModelViewSet):
    queryset = StudentScheduleS.objects.all()
    serializer_class = StudentScheduleSSerializer


# class TestOne(APIView):
#     @staticmethod
#     def get(request):
#         test = StudentScheduleS.objects.all()
#         return Response(status=200, data={'test': 90})
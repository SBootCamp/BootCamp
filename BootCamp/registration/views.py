import json

import generics as generics
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, request, status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from .serializers import ScheduleSSerializer, StudentsSerializer, StudentScheduleSSerializer, ForPutSerializer, \
    ForPostSerializer
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
    some3 = StudentScheduleS.objects.all()
    res = '<h1>Расписание студентов</h1>'

    import datetime

    d1 = datetime.datetime.today()
    d1 = d1 + datetime.timedelta(days=1)

    for i in range(30):
        d2 = d1 + datetime.timedelta(days=i)
        res += f'<div> {d2.strftime("%Y %A %d %B ")}{[item.name for item in some]}</div>'
    return HttpResponse(res)

class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentsSerializer

    def put(self, id):
        change = Student.objects.get(id=id)
        serializer = StudentsSerializer(change, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    def delete(self, id):
        change = Student.objects.get(id=id)
        serializer = StudentsSerializer(change, data=request.data)
        if serializer.is_valid():
            change.delete()
        return Response(status=status.HTTP_200_OK)


class ScheduleAPIView(APIView):

    def get(self, request):
        bb = Student.objects.all()
        res = StudentsSerializer(bb, many=True)
        return Response(data=res.data)

class OneStudentSchedule(APIView):

    def get_queryset(self, *args, **kwargs):
        res = Student.objects.all()
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
    def post(request: Request, id=None) -> Response:
        try:
            answer = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response(status=400, data={'error': 'STUDENT not found'})
        ser = ForPostSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        b = ScheduleS.objects.get_or_create(day_of_week=data.get('day_of_week'))
        c = answer.schedule.add(b)
        c.save()
        return Response(c.data)

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

    def delete(self, request, id=None):
        answer = self.get_object(id or request.query_params.get('id'))
        answer.delete()
        return Response(status=status.HTTP_200_OK)

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
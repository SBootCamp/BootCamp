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

from .serializers import ScheduleSSerializer, StudentsSerializer, StudentScheduleSSerializer, ForPutSerializer, \
    ForPostSerializer, MentorSerializer
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
    student_ = Student.objects.all()
    schedule_ = ScheduleS.objects.all()
    student_schedule_ = StudentScheduleS.objects.all()
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
    queryset = Student.objects.all()
    serializer_class = StudentsSerializer

    def delete(self, id):
        change = Student.objects.get(id=id)
        serializer = StudentsSerializer(change, data=request.data)
        if serializer.is_valid():
            change.delete()
        return Response(status=status.HTTP_200_OK)


class ScheduleAPIView(APIView):

    def get(self, request):
        queryset = Student.objects.all()
        res = StudentsSerializer(queryset, many=True)
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
    def post(request, id=None):
        try:
            answer = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response(status=400, data={'error': 'STUDENT not found'})
        ser = ForPostSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        b = ScheduleS.objects.create(day_of_week=data.get('day_of_week'), pk=data.get('id'))
        c = answer.schedule.add(b)
        try:
            c.save()
        except AttributeError:
            return Response(status=status.HTTP_201_CREATED)
        return Response(c.data, status=status.HTTP_201_CREATED)

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
            schedule_for_del = ScheduleS.objects.get(pk=schedule_s_id)
            schedule_for_del.delete()
        except ScheduleS.DoesNotExist:
            return Response(status=400, data={'error': 'schedule not found'})
        return Response(status=status.HTTP_200_OK, data={'deleted': 'schedule was deleted'})

class ScheduleSViewSet(viewsets.ModelViewSet):
    queryset = ScheduleS.objects.all()
    serializer_class = ScheduleSSerializer


class StudentScheduleSViewSet(viewsets.ModelViewSet):
    queryset = StudentScheduleS.objects.all()
    serializer_class = StudentScheduleSSerializer


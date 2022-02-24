from rest_framework import serializers
from .models import StudentScheduleS, ScheduleS, Student


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name')


class ScheduleSSerializer(serializers.ModelSerializer):
    names = StudentsSerializer(many=True, read_only=True)

    class Meta:
        model = ScheduleS
        fields = ('id', 'day_of_week', 'time_in','time_out', 'here', 'names')


class StudentScheduleSSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentScheduleS
        fields = ('notes', 'names', 'days',)

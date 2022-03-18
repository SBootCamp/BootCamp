from rest_framework import serializers
from .models import ScheduleS, Student


class ScheduleSSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    day_of_week = serializers.DateField()
    time_in = serializers.TimeField()
    time_out = serializers.TimeField()

class StudentsSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=100)
    schedule = ScheduleSSerializer(required=False, many=True)

class MentorSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=100)
    schedule = ScheduleSSerializer(required=False, many=True)


class ForPostSerializer(serializers.Serializer):

    day_of_week = serializers.DateField()
    time_in = serializers.TimeField(required=False)
    time_out = serializers.TimeField(required=False)

class ForPutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    day_of_week = serializers.DateField(required=False)
    time_in = serializers.TimeField(required=False)
    time_out = serializers.TimeField(required=False)


# class StudentScheduleSSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = StudentScheduleS
#         fields = ('notes', 'student', 'schedule',)



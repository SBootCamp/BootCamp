from rest_framework import serializers
from .models import StudentScheduleS, ScheduleS, Student


# class StudentsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ('id', 'name')
#
#
# class ScheduleSSerializer(serializers.ModelSerializer):
#     names = StudentsSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = ScheduleS
#         fields = ('id', 'day_of_week', 'time_in','time_out', 'here', 'names')


class ScheduleSSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    day_of_week = serializers.DateField()
    time_in = serializers.TimeField()
    time_out = serializers.TimeField()

class StudentsSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=100)
    schedule = ScheduleSSerializer(many=True)


class ForPostSerializer(serializers.Serializer):

    day_of_week = serializers.DateField()
    time_in = serializers.TimeField(required=False)
    time_out = serializers.TimeField(required=False)

class ForPutSerializer(serializers.Serializer):
    id = serializers.IntegerField
    day_of_week = serializers.DateField(required=False)
    time_in = serializers.TimeField(required=False)
    time_out = serializers.TimeField(required=False)


class StudentScheduleSSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentScheduleS
        fields = ('notes', 'names', 'days',)


# class ScheduleModel:
#     def __init__(self, name, day):
#         self.name = name
#         self.day = day
#
# class ScheduleNewSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     day = serializers.DateField()



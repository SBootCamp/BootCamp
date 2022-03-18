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



class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()


def validators_number_phone(value):
    if not value.isdigit():
        raise serializers.ValidationError("Номер телефона должен состоять только из цифр")


class ProfileSerializerView(serializers.Serializer):
    user = UserSerializer(required=True)
    github = serializers.CharField(max_length=50)
    number_phone = serializers.CharField(max_length=11, validators=[validators_number_phone])
    password = serializers.CharField(max_length=50)

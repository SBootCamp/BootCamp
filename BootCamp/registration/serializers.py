from rest_framework import serializers


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

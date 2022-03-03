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

    # def create(self, validated_data):
    #     user_data = validated_data.pop('user', None)
    #     if user_data:
    #         user = User.objects.get_or_create(**user_data)[0]
    #         validated_data['user'] = user
    #         user.set_password(validated_data['password'])
    #         user.save()
    #     return Profile.objects.create(**validated_data)

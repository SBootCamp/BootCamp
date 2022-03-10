from rest_framework import serializers
from .models import Node, User, Event
from datetime import datetime, timedelta


class EventSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=50, allow_blank=True)
    node_id = serializers.CharField(max_length=150, allow_blank=True)
    status = serializers.CharField(max_length=300, allow_blank=True)

    def create(self, validated_data):
        validated_data["user_id"] = User.objects.filter(username=validated_data["user_id"])[0]
        validated_data["node_id"] = Node.objects.filter(name=validated_data["node_id"])[0]
        validated_data["startdate"] = datetime.now()
        deadline = Node.objects.filter(name=validated_data["node_id"])[0].deadline
        validated_data["enddate"] = datetime.now() + timedelta(days=deadline)
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print(type(instance))
        print(validated_data)
        if instance:
            # Update existing instance
            instance.user_id = User.objects.filter(username=validated_data.get('user_id', instance.user_id))[0]
            instance.node_id = Node.objects.filter(name=validated_data.get('node_id', instance.node_id))[0]
            instance.status = validated_data.get('status', instance.status)
            instance.save()
        return instance


class EventListSerializer(EventSerializer):
    startdate = serializers.DateTimeField()
    enddate = serializers.DateTimeField()
    pk = serializers.IntegerField()

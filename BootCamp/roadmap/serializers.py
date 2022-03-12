from rest_framework import serializers
from .models import Node, User, Event
from datetime import datetime, timedelta


class EventSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=50, allow_blank=True)
    node_id = serializers.CharField(max_length=150, allow_blank=True)
    status = serializers.CharField(max_length=300, allow_blank=True)

class EventListSerializer(EventSerializer):
    startdate = serializers.DateTimeField()
    enddate = serializers.DateTimeField()
    pk = serializers.IntegerField()

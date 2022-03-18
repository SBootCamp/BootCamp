from datetime import datetime, timedelta
from .choices import EventStatus
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Node, User, Event
from .serializers import EventSerializer, EventListSerializer


class index(APIView):
    def get(self, request):
        try:
            user = User.objects.get(pk=request.user.pk)
        except User.DoesNotExists:
            return Response({"error": "Пользователь не найден"}, status=409)
        good_list = list(Event.objects.filter(user_id=user, status=EventStatus.success).values_list("node_id__name", flat=True))
        ready_list = list(Event.objects.filter(user_id=user, status=EventStatus.ready).values_list("node_id__name", flat=True))
        start_list = list(Event.objects.filter(user_id=user, status=EventStatus.start).values_list("node_id__name", flat=True))
        return render(
            request,
            'tree.html',
            context={'nodes': Node.objects.all(), 'good': good_list, 'ready': ready_list, 'start': start_list},
        )


class indexUsers(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExists:
            return Response({"error": "Пользователь не найден"}, status=409)
        good_list = list(Event.objects.filter(user_id=user, status=EventStatus.success).values_list("node_id__name", flat=True))
        ready_list = list(Event.objects.filter(user_id=user, status=EventStatus.ready).values_list("node_id__name", flat=True))
        start_list = list(Event.objects.filter(user_id=user, status=EventStatus.start).values_list("node_id__name", flat=True))
        return render(
            request,
            'tree.html',
            context={'nodes': Node.objects.all(), 'good': good_list, 'ready': ready_list, 'start': start_list},
        )


class ViewEvent(APIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request):
        user = User.objects.get(pk=request.user.pk)
        query = Event.objects.filter(user_id=user)
        serializer = EventListSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request):
        events = request.data
        serializer = EventSerializer(data=events)
        serializer.is_valid(raise_exception=True)
        Event.objects.create(user_id=User.objects.get(username=events["user_id"]),
                             node_id=Node.objects.get(name=events["node_id"]),
                             status=events["status"],
                             startdate=datetime.now(),
                             enddate=datetime.now() + timedelta(
                                 days=Node.objects.get(name=events["node_id"]).deadline)
                             )
        return Response(serializer.data)


class DetailEvent(APIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, pk):
        user = User.objects.get(pk=request.user.pk)
        query = Event.objects.get(user_id=user, pk=pk)
        serializer = EventListSerializer(query)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            query = Event.objects.get(pk=pk)
        except Event.DoesNotExists:
            return Response({"error": "Запись не найдена"}, status=400)
        events = request.data
        serializer = EventSerializer(data=events)
        serializer.is_valid(raise_exception=True)
        query.user_id = User.objects.get(username=events.get('user_id', query.user_id))
        query.node_id = Node.objects.get(name=events.get('node_id', query.node_id))
        query.status = events.get('status', query.status)
        query.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExists:
            return Response({"error": "Запись не найдена"}, status=400)
        event.delete()
        return Response({"message": "Удалил"}, status=204)


class ListAcceptEvents(APIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request):
        query = Event.objects.filter(status=EventStatus.ready)
        serializer = EventListSerializer(query, many=True)
        return Response(serializer.data)


class DetailAcceptEvents(APIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, pk):
        query = Event.objects.get(pk=pk)
        serializer = EventListSerializer(query)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            query = Event.objects.get(pk=pk)
        except Event.DoesNotExists:
            return Response({"error": "Запись не найдена"}, status=400)
        events = request.data
        serializer = EventSerializer(data=events)
        serializer.is_valid(raise_exception=True)
        query.user_id = User.objects.get(username=events.get('user_id', query.user_id))
        query.node_id = Node.objects.get(name=events.get('node_id', query.node_id))
        query.status = events.get('status', query.status)
        query.save()
        return Response(serializer.data)

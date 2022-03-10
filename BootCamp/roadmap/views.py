from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


def index(request):
    user = User.objects.filter(username=request.user.username)[0]
    query = Event.objects.filter(user_id=user)
    newlist = [i.node_id.name for i in query]

    return render(
        request,
        'tree.html',
        context={'nodes': Node.objects.all(), 'list': newlist},
    )


def indexUsers(request, pk):
    user = User.objects.filter(pk=pk)[0]
    query = Event.objects.filter(user_id=user)
    newlist = [i.node_id.name for i in query]

    return render(
        request,
        'tree.html',
        context={'nodes': Node.objects.all(), 'list': newlist},
    )


class ViewEvent(APIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.filter(username=request.user.username)[0]
            query = Event.objects.filter(user_id=user)
            serializer = EventListSerializer(query, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'error'})

    def post(self, request):
        if request.user.is_authenticated:
            user = User.objects.filter(username=request.user.username)[0]
            query = Event.objects.filter(user_id=user)
            events = request.data
            print(events)
            serializer = EventSerializer(data=events)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        return Response(serializer.data)


class DetailEvent(APIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, pk):
        if request.user.is_authenticated:
            user = User.objects.filter(username=request.user.username)[0]
            query = Event.objects.filter(user_id=user, pk=pk)[0]
            serializer = EventListSerializer(query)
            return Response(serializer.data)
        else:
            return Response({'error': 'error'})

    def put(self, request, pk):
        print(request.user)
        if request.user.is_authenticated:
            user = User.objects.filter(username=request.user.username)[0]
            query = get_object_or_404(Event.objects.all(), pk=pk)
            events = request.data
            serializer = EventSerializer(instance=query, data=events, partial=True)
            if serializer.is_valid(raise_exception=True):
                query = serializer.save()
            return Response(serializer.data)
        else:
            return Response({'error': 'Авторизуйтесь для этого действия'})

    def delete(self, request, pk):
        event = get_object_or_404(Event.objects.all(), pk=pk)
        event.delete()
        return Response({"message": "Удалил".format(pk)}, status=204)


class ListAcceptEvents(APIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.filter(username=request.user.username)[0]
            query = Event.objects.filter()
            serializer = EventListSerializer(query, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'error'})


class DetailAcceptEvents(APIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, pk):
        if request.user.is_authenticated:
            user = User.objects.filter(username=request.user.username)[0]
            query = Event.objects.filter(user_id=user, pk=pk)[0]
            serializer = EventListSerializer(query)
            return Response(serializer.data)
        else:
            return Response({'error': 'error'})

    def put(self, request, pk):
        if request.user.is_authenticated:
            user = User.objects.filter(username=request.user.username)[0]
            query = get_object_or_404(Event.objects.all(), pk=pk)
            events = request.data
            serializer = EventSerializer(instance=query, data=events, partial=True)
            if serializer.is_valid(raise_exception=True):
                query = serializer.save()
            return Response(serializer.data)

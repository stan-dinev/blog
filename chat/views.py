from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Message
from .serializers import MessageSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.parsers import JSONParser
from online_users.models import OnlineUserActivity
from datetime import timedelta

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect('chat-api:chats')
    if not request.user.is_authenticated:
        return redirect('accounts-api:login')
    if request.method == 'GET':
        return render(request, 'index.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error": "User does not exist"}')
        return redirect('chat-api:chats')


@csrf_protect
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def chat_view(request):
    """Render the template with required context variables"""
    if not request.user.is_authenticated:
        return redirect('accounts-api:login')
    if request.method == "GET":
        user_activity_objects = OnlineUserActivity.get_user_activities(timedelta(minutes=60))
        active_users = (user for user in user_activity_objects)
        return render(request, 'chat.html',
                      {'users': User.objects.exclude(username=request.user.username),
                       'active_users': active_users})


def message_view(request, sender, receiver):
    """Render the template with required context variables"""
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'messages.html',
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})


class MessageList(ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, sender=None, receiver=None):
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

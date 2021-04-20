from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>/', views.message_view, name='chat'),
    path('messages/<int:sender>/<int:receiver>/', views.message_list, name='message-detail'),
    path('messages/', views.message_list, name='message-list'),

]

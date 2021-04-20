from django.urls import path, re_path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'questions', views.QuestionCreateList, basename='Question')

urlpatterns = [
    path('questions/', views.QuestionCreateList.as_view(), name='questions'),
    re_path('^question/(?P<pk>\d+)/$', views.QuestionDetails.as_view(), name='questions_details'),
    re_path('^question/(?P<pk>\d+)/answer/(?P<answer_pk>\d+)/$', views.AnswerDetail.as_view(), name='answer'),
]

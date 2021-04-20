from rest_framework import serializers
from . models import Question, Answer
from rest_framework.serializers import HyperlinkedIdentityField


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('id', 'author', 'content', 'likes', 'dislikes',)


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    url = HyperlinkedIdentityField(
        view_name='forum-api:questions_details',
        lookup_field='pk'
    )

    class Meta:
        model = Question
        fields = ('id', 'url', 'author', 'question', 'answers')

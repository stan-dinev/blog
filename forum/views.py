from django.shortcuts import render
from . models import Question, Answer
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from . serializers import QuestionSerializer, AnswerSerializer
from django.http import Http404
# Create your views here.


class MethodSerializerView(object):
    """
    Utility class for get different serializer class by method.
    For example:
    method_serializer_classes = {
        ('GET', ): MyModelListViewSerializer,
        ('PUT', 'PATCH'): MyModelCreateUpdateSerializer
    }
    """
    method_serializer_classes = None

    def get_serializer_class(self):
        assert self.method_serializer_classes is not None, (
            'Expected view %s should contain method_serializer_classes '
            'to get right serializer class.' %
            (self.__class__.__name__, )
        )
        for methods, serializer_cls in self.method_serializer_classes.items():
            if self.request.method in methods:
                return serializer_cls

        raise exceptions.MethodNotAllowed(self.request.method)


def validate_and_return_response(serializer):
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionList(APIView):

    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetails(APIView):

    def get_object(self, pk):
        try:
            question = Question.objects.get(pk=pk)
            return question
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        question = self.get_object(pk=pk)
        serializer = QuestionSerializer(question, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        question = self.get_object(pk=pk)
        serializer = QuestionSerializer(question, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id):
        question = self.get_object(pk=question_id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerDetail(APIView):

    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, pk, answer_pk):
        full_request_url = request.build_absolute_uri()
        if 'dislike' in full_request_url:
            answer = self.get_object(pk=answer_pk)
            answer.dislikes += 1
            answer.save()
            serializer = AnswerSerializer(answer)
            return Response(serializer.data)
        elif 'like' in full_request_url:
            answer = self.get_object(pk=answer_pk)
            answer.likes += 1
            answer.save()
            serializer = AnswerSerializer(answer)
            return Response(serializer.data)
        else:
            answer = self.get_object(pk=answer_pk)
            serializer = AnswerSerializer(answer)
            return Response(serializer.data)

    def put(self, request, pk, answer_pk):
        answer = self.get_object(pk=answer_pk)
        serializer = AnswerSerializer(answer, data=request.data)

        validate_and_return_response(serializer)

    def patch(self, request, pk, answer_pk):
        answer = self.get_object(pk=answer_pk)
        serializer = AnswerSerializer(answer, data=request.data)

        validate_and_return_response(serializer)

    def delete(self, request, pk, answer_pk):
        answer = self.get_object(pk=answer_pk)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionCreateList(ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer



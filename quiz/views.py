from django.http import HttpResponse, JsonResponse
from rest_framework import mixins, viewsets, generics, views, serializers, status
from rest_framework.response import Response

from .dto import QuizPassDto
from .services import QuizResultService


class QuizListApi(views.APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField(source="uuid")
        title = serializers.CharField()
        questions_count = serializers.SerializerMethodField()

        def get_questions_count(self, obj):
            return len(obj.questions)

    def get(self, request):
        quizes = QuizResultService.get_quiz_list()
        data = self.OutputSerializer(quizes, many=True).data
        return Response(data)


class QuizDetailApi(views.APIView):
    class QuizOutputSerializer(serializers.Serializer):
        class QuestionOutputSerializer(serializers.Serializer):
            class ChoiceOutputSerializer(serializers.Serializer):
                id = serializers.CharField(source="uuid")
                text = serializers.CharField()

            id = serializers.CharField(source="uuid")
            text = serializers.CharField()
            choices = ChoiceOutputSerializer(many=True)

        id = serializers.CharField(source="uuid")
        title = serializers.CharField()
        questions = QuestionOutputSerializer(many=True)

    def get(self, request, quiz_pass_id):
        quiz = QuizResultService.get_passing_quiz(quiz_pass_id)
        data = self.QuizOutputSerializer(quiz).data
        return Response(data)


class StartQuizApi(views.APIView):
    class OutputSerializer(serializers.Serializer):
        quiz_pass_id = serializers.CharField(source="uuid")

    def post(self, request, quiz_id):
        quiz_pass_dto = QuizResultService.start_quiz(quiz_id)
        data = self.OutputSerializer(quiz_pass_dto).data
        return Response(data)


class SubmitQuizApi(views.APIView):
    class InputSerializer(serializers.Serializer):
        question_id = serializers.CharField()
        choice_ids = serializers.ListSerializer(child=serializers.CharField())

    class QuizPassOutputSerializer(serializers.Serializer):
        class QuestionOutputSerializer(serializers.Serializer):
            class ChoiceOutputSerializer(serializers.Serializer):
                id = serializers.CharField(source="uuid")
                is_correct = serializers.BooleanField()

            id = serializers.CharField(source="uuid")
            choices = ChoiceOutputSerializer(many=True)

        id = serializers.CharField(source="uuid")
        result = serializers.FloatField()
        questions = serializers.SerializerMethodField()

        def get_questions(self, obj):
            return self.QuestionOutputSerializer(obj.quiz.questions, many=True).data

    def post(self, request, quiz_pass_id):
        question_answers = self.InputSerializer(request.data, many=True).data
        quiz_pass_dto = QuizResultService.submit_quiz_pass(quiz_pass_id, question_answers)
        data = self.QuizPassOutputSerializer(quiz_pass_dto).data
        return Response(data)

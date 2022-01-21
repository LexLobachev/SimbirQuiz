import itertools
from typing import List, NamedTuple

from django.core.management.base import BaseCommand

from quiz.dto import ChoiceDTO, QuestionDTO
from quiz.models import Quiz, Question, Choice


class ChoiceSeedDto(NamedTuple):
    text: str
    is_correct: bool


class Command(BaseCommand):
    help = "seed database"

    def create_question(self, quiz_id, text: str, choices: List[ChoiceSeedDto]):
        quest = Question.objects.create(text=text, quiz_id=quiz_id)
        for ch in choices:
            ch_model = Choice.objects.create(text=ch.text, is_correct=ch.is_correct, question_id=quest.uuid)
            quest.choice_set.add(ch_model)
        return quest

    def handle(self, *args, **options):
        quiz_id = Quiz.objects.create(title="Тест на знания Python").uuid

        q1 = self.create_question(quiz_id, "Какой вариант ответа не выдаст ошибку при запуске проекта?",
                                  [ChoiceSeedDto("int num = 2", False),
                                   ChoiceSeedDto("num = float(2)", True),
                                   ChoiceSeedDto("int num = 2", False),
                                   ChoiceSeedDto("нет подходящего ответа", False)])

        q2 = self.create_question(quiz_id, "Как получить данные от пользователя?",
                                  [ChoiceSeedDto("Использовать метод input() ", True),
                                   ChoiceSeedDto("Использовать метод get()", False),
                                   ChoiceSeedDto("Использовать метод read()", False),
                                   ChoiceSeedDto("Использовать метод readLine()", False)])

        q3 = self.create_question(quiz_id, "Какая библиотека отвечает за время?",
                                  [ChoiceSeedDto("time", True),
                                   ChoiceSeedDto("Time", False),
                                   ChoiceSeedDto("localtime", False),
                                   ChoiceSeedDto("нет подходящего ответа", False)])

        q4 = self.create_question(quiz_id, "Какое(ие) значение(я) получит a? a = 2,3",
                                  [ChoiceSeedDto("12", False),
                                   ChoiceSeedDto("6", False),
                                   ChoiceSeedDto("3", True),
                                   ChoiceSeedDto("2", True), ])

        q5 = self.create_question(quiz_id, "Укажите все правильные способы использования print:",
                                  [ChoiceSeedDto("print(5)", True),
                                   ChoiceSeedDto("print 5", False),
                                   ChoiceSeedDto("print('5' * 5)", True),
                                   ChoiceSeedDto("нет подходящего ответа", False)])

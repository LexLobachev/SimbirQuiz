import uuid

from django.db import models


class Quiz(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=101)

    class Meta:
        db_table = 'quiz'


class Question(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=1000)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    class Meta:
        db_table = 'question'


class Choice(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=1000)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField()

    class Meta:
        db_table = 'choice'


class QuizPass(models.Model):

    class State(models.IntegerChoices):
        Active = 1
        Done = 2

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.DO_NOTHING)
    state = models.IntegerField(choices=State.choices, default=State.Active)

    class Meta:
        db_table = 'quiz_pass'


class Answer(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quizPass = models.ForeignKey(QuizPass, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    choice = models.ForeignKey(Choice, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'answer'

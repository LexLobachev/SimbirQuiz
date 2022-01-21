from django.db.transaction import atomic

from .dto import ChoiceDTO, QuestionDTO, QuizDTO, AnswerDTO, AnswersDTO, QuizPassDto, QuizPassState
from typing import List

from .models import Quiz, QuizPass, Question, Choice, Answer


class QuizResultService():
    def __init__(self, quiz_dto: QuizDTO, answers_dto: AnswersDTO):
        self.quiz_dto = quiz_dto
        self.answers_dto = answers_dto

    def get_result(self) -> float:
        quest_count = len(self.quiz_dto.questions)
        correct_ans_count = 0

        for quest in self.quiz_dto.questions:
            correct_choice_uuids = list(map(lambda c: c.uuid, filter(lambda c: c.is_correct, quest.choices)))
            quest_ans = next(filter(lambda ans: ans.question_uuid == quest.uuid, self.answers_dto.answers), None)
            fault_choices = filter(lambda ch: ch not in correct_choice_uuids, quest_ans.choices if quest_ans else [])
            if quest_ans and len(quest_ans.choices) == len(correct_choice_uuids) and not next(fault_choices, None):
                correct_ans_count += 1

        return round(correct_ans_count / quest_count, 2)

    @classmethod
    def get_quiz_list(cls) -> List[QuizDTO]:
        return list(map(cls._map_quiz_dto, Quiz.objects.all()))

    @classmethod
    def get_passing_quiz(cls, quiz_pass_uuid) -> QuizDTO:
        return cls._map_quiz_dto(QuizPass.objects.get(pk=quiz_pass_uuid).quiz)

    @classmethod
    def start_quiz(cls, quiz_uuid: str) -> QuizPassDto:
        quiz = Quiz.objects.get(pk=quiz_uuid)
        quiz_pass = QuizPass(quiz=quiz, )
        quiz_pass.state = QuizPass.State.Active
        quiz_pass.save()
        return cls._map_quiz_pass_dto(quiz_pass)

    @classmethod
    def submit_quiz_pass(cls, quiz_pass_uuid: str, question_answers) -> QuizPassDto:
        quiz_pass = QuizPass.objects.get(pk=quiz_pass_uuid)
        if quiz_pass.state == QuizPass.State.Done:
            raise Exception('Quiz has already been submitted')

        for quest_ans in question_answers:
            for ch_id in quest_ans['choice_ids']:
                answer = Answer(question_id=quest_ans['question_id'], quizPass_id=quiz_pass_uuid, choice_id=ch_id)
                answer.save()

        quiz_pass.state = QuizPass.State.Done
        quiz_pass.save()

        return cls._map_quiz_pass_dto(quiz_pass)

    @classmethod
    def _map_quiz_dto(cls, quiz_model: Quiz) -> QuizDTO:
        return QuizDTO(
            uuid=quiz_model.uuid,
            title=quiz_model.title,
            questions=list(map(cls._map_question_dto, quiz_model.question_set.all()))
        )

    @classmethod
    def _map_question_dto(cls, quest_model: Question) -> QuestionDTO:
        return QuestionDTO(
            uuid=quest_model.uuid,
            text=quest_model.text,
            choices=list(map(cls._map_choice, quest_model.choice_set.all()))
        )

    @classmethod
    def _map_choice(cls, choice_model: Choice) -> ChoiceDTO:
        return ChoiceDTO(
            uuid=choice_model.uuid,
            text=choice_model.text,
            is_correct=choice_model.is_correct
        )

    @classmethod
    def _map_quiz_pass_dto(cls, quiz_pass_model: QuizPass) -> QuizPassDto:
        quest_id_to_choice = map(lambda ans: (ans.question.uuid, ans.choice.uuid), quiz_pass_model.answer_set.all())
        quest_id_to_choices: dict[str, List[str]] = dict()
        for quest_id, choice_id in quest_id_to_choice:
            if quest_id in quest_id_to_choices:
                quest_id_to_choices[quest_id].append(choice_id)
            else:
                quest_id_to_choices[quest_id] = [choice_id]

        quiz = cls._map_quiz_dto(quiz_pass_model.quiz)
        answers = AnswersDTO(
            quiz_uuid=quiz_pass_model.quiz_id,
            answers=list(
                map(
                    lambda quiz_id: AnswerDTO(question_uuid=quiz_id, choices=quest_id_to_choices[quiz_id])
                    , quest_id_to_choices)
            )
        )
        result = QuizResultService(quiz, answers).get_result() if quiz_pass_model.state == QuizPassState.DONE else None

        quiz_pass_dto = QuizPassDto(
            uuid=quiz_pass_model.uuid,
            quiz=quiz,
            state=cls._pass_model_state_to_dto_state(quiz_pass_model.state),
            answers=answers,
            result=result
        )

        return quiz_pass_dto

    @classmethod
    def _pass_model_state_to_dto_state(cls, model_state: int) -> QuizPassState or None:
        if model_state == QuizPass.State.Active:
            return QuizPassState.ACTIVE
        elif model_state == QuizPass.State.Done:
            return QuizPassState.DONE
        return None

from typing import List, NamedTuple


class ChoiceDTO(NamedTuple):
    uuid: str
    text: str
    is_correct: bool


class QuestionDTO(NamedTuple):
    uuid: str
    text: str
    choices: List[ChoiceDTO]


class QuizDTO(NamedTuple):
    uuid: str
    title: str
    questions: List[QuestionDTO]


class AnswerDTO(NamedTuple):
    question_uuid: str
    choices: List[str]


class AnswersDTO(NamedTuple):
    quiz_uuid: str
    answers: List[AnswerDTO]


class QuizPassState:
    ACTIVE = 1,
    DONE = 2


class QuizPassDto(NamedTuple):
    uuid: str
    state: QuizPassState
    quiz: QuizDTO
    answers: AnswersDTO
    result: float or None




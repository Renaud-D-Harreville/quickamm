from abc import ABC, abstractmethod
from pathlib import Path

from qa.models.models import MCQAnswer, BasicMCQData
import numpy as np
from typing import TypeVar
from pydantic import BaseModel
import random

class MultipleChoiceQuestion(BaseModel):
    question: str
    answers: list[str]
    correct_indexes: list[int]
    image_path: str | None = None
    answer_description: str | None = None
    question_id: str | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.question_id:
            self.question_id = self.hash()

    def hash(self) -> str:
        if self.image_path:
            return f"{self.question} src='{self.image_path}'"
        return self.question

    def is_correct_answer(self, answer_indexes: list[int]) -> bool:
        if len(answer_indexes) != len(self.correct_indexes):
            return False
        for elem in answer_indexes:
            if elem not in self.correct_indexes:
                return False
        return True

    def to_mcq_data(self) -> BasicMCQData:
        mcq_answers = []
        for i, answer in enumerate(self.answers):
            a = MCQAnswer(
                text=answer,
                is_true= i in self.correct_indexes
            )
            mcq_answers.append(a)

        return BasicMCQData(
            question=self.question,
            image_path=self.image_path,
            answers=mcq_answers,
            description=self.answer_description
        )

class MCQModel(BaseModel):
    topics: list[str]
    question: str
    image_path: str | None = None
    correct_answers: list[str]
    wrong_answers: list[str]
    long_description: str | None = None


    def is_under_topic(self, topic: str) -> bool:
        for t in self.topics:
            # Search if for example t "AMM/Level2/Level3" starts with input topic "AMM/Level2"
            if t.startswith(topic):
                return True
        return False

    def is_qcm_ok(self) -> bool:
        if len(self.wrong_answers) >= 3 and len(self.correct_answers) >= 1:
            return True
        return False

    def _get_nb_true_answers(self, nb_true_answers: int = None) -> int:
        if not nb_true_answers:
            nb_true_answers = random.choices((1, 2), weights=(1, 1 / 6))[0] if len(self.correct_answers) > 1 else 1
        elif nb_true_answers > 2:
            nb_true_answers = 2
        elif nb_true_answers <= 0:
            nb_true_answers = 1
        return nb_true_answers

    @staticmethod
    def _shuffle_answers(true_answers: list[str], wrong_answers: list[str]) -> tuple[list[str], list[int]]:
        random.shuffle(true_answers)
        random.shuffle(wrong_answers)
        correct_indexes = list(np.random.choice(4, size=len(true_answers), replace=False))
        correct_indexes.sort()
        for i, index in enumerate(correct_indexes):
            wrong_answers.insert(index, true_answers[i])
        return wrong_answers, correct_indexes

    def make_random_mcq(self, nb_true_answers: int = None) -> MultipleChoiceQuestion:
        nb_true_answers = self._get_nb_true_answers(nb_true_answers)
        # Need the use of numpy to have a choice without replacement.
        true_answers = list(np.random.choice(self.correct_answers, size=nb_true_answers, replace=False))
        wrong_answers = list(np.random.choice(self.wrong_answers, size=4 - nb_true_answers, replace=False))
        sorted_answers, correct_indexes = self._shuffle_answers(true_answers, wrong_answers)
        question = MultipleChoiceQuestion(
            question=self.question,
            answers=sorted_answers,
            image_path= self.image_path,
            correct_indexes=correct_indexes,
            answer_description=self.long_description
        )
        return question


SurroundingMCQObjectClass: TypeVar = TypeVar("SurroundingMCQObjectClass")


class AbstractMCQFactory(ABC):

    @abstractmethod
    def _topic_weight(self, topic: str) -> int:
        pass

    def is_under_topic(self, topic: str) -> bool:
        for t in self.topics:
            # Search if for example t "AMM/Level2/Level3" starts with input topic "AMM/Level2"
            if t.startswith(topic):
                return True
        return False

    def topic_weight(self, topic: str) -> int:
        if not self.is_under_topic(topic):
            return 0
        return self._topic_weight(topic)

    @property
    @abstractmethod
    def topics(self):
        pass

    def get_all_level_topics(self) -> list[str]:
        all_level_topics = []
        for topic in self.topics:
            split_topic = topic.split('/')
            for i in range(len(split_topic)):
                sub_topic = "/".join(split_topic[:i+1])
                all_level_topics.append(sub_topic)
        return list(set(all_level_topics))

    @abstractmethod
    def related_topics(self, surrounding_mcq_object: SurroundingMCQObjectClass) -> list[str]:
        pass

    @abstractmethod
    def get_question(self, surrounding_mcq_object: SurroundingMCQObjectClass) -> str:
        pass

    def get_image_path(self, surrounding_mcq_object: SurroundingMCQObjectClass) -> Path | str | None:
        return None

    @abstractmethod
    def get_random_surrounding_question_object(self, topic: str) -> SurroundingMCQObjectClass:
        pass

    @abstractmethod
    def get_possible_true_answers(self, surrounding_mcq_object: SurroundingMCQObjectClass) -> list[str]:
        pass

    @abstractmethod
    def get_possible_false_answers(self, surrounding_mcq_object: SurroundingMCQObjectClass) -> list[str]:
        pass

    def get_explanation(self, surrounding_mcq_object: SurroundingMCQObjectClass) -> str | None:
        return None

    def get_random_mcq_model(self, topic: str) -> MCQModel:
        surrounding_mcq_object = self.get_random_surrounding_question_object(topic)
        return MCQModel(
            topics=self.related_topics(surrounding_mcq_object),
            question=self.get_question(surrounding_mcq_object),
            image_path=self.get_image_path(surrounding_mcq_object),
            correct_answers=self.get_possible_true_answers(surrounding_mcq_object),
            wrong_answers=self.get_possible_false_answers(surrounding_mcq_object),
            long_description=self.get_explanation(surrounding_mcq_object)
        )

    def make_random_mcq(self, topic: str) -> MultipleChoiceQuestion:
        mcq_model = self.get_random_mcq_model(topic)
        mcq = mcq_model.make_random_mcq()
        return mcq

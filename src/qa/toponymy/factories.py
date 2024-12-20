from abc import abstractmethod

from qa.toponymy.models import ToponymyWord, ToponymyList
from qa.mcq_db.models import MCQAnswer
from qa.common.base_factory import AbstractMCQFactory
from abc import ABC


class BaseToponymyMCQFactory(AbstractMCQFactory, ABC):
    TOPICS = ["AMM", "Probatoire AMM", "Le milieu montagnard", "Toponymie"]

    def __init__(self, toponymy: ToponymyList):
        self.toponymy: ToponymyList = toponymy

    def get_questions_with_topics(self, topics: list[str]) -> list[ToponymyWord]:
        if all([topic in self.TOPICS for topic in topics]):
            return self.toponymy.words
        return list()

    def get_answers(self, surrounding_mcq_object: ToponymyWord) -> list[MCQAnswer]:
        correct_answer = self.get_true_answer(surrounding_mcq_object)
        wrong_answers = self.get_possible_false_answers(surrounding_mcq_object)
        answers = [correct_answer] + wrong_answers
        return answers

    @abstractmethod
    def _to_mcq_answer(self, toponymy_word: ToponymyWord, is_true: bool) -> MCQAnswer:
        pass

    def get_true_answer(self, surrounding_mcq_object: ToponymyWord) -> MCQAnswer:
        return self._to_mcq_answer(surrounding_mcq_object, True)

    def get_possible_false_answers(self, surrounding_mcq_object: ToponymyWord) -> list[str]:
        answers = [self._to_mcq_answer(word, False) for word in self.toponymy.words
                   if surrounding_mcq_object != word]
        return answers

    def get_explanation(self, surrounding_mcq_object: ToponymyWord) -> str | None:
        return surrounding_mcq_object.get_basic_description()


class ToponymyToWordMCQFactory(BaseToponymyMCQFactory):
    TOPICS = BaseToponymyMCQFactory.TOPICS + ["Toponyme vers traduction"]

    def get_question(self, surrounding_mcq_object: ToponymyWord) -> str:
        question = f"Que signifient ces mots : {surrounding_mcq_object.get_words()}"
        return question

    def _to_mcq_answer(self, toponymy_word: ToponymyWord, is_true: bool) -> MCQAnswer:
        mcq_answer = MCQAnswer(
            text=toponymy_word.get_str_traduction(),
            is_true=is_true,
            explanation=toponymy_word.get_basic_description()
        )
        return mcq_answer


class WordToToponymyMCQFactory(BaseToponymyMCQFactory):
    TOPICS = BaseToponymyMCQFactory.TOPICS + ["Traduction vers toponyme"]


    def get_question(self, surrounding_mcq_object: ToponymyWord) -> str:
        question = f"Quelle sont les toponymes possibles de : {surrounding_mcq_object.get_str_traduction()}"
        return question


    def _to_mcq_answer(self, toponymy_word: ToponymyWord, is_true: bool) -> MCQAnswer:
        mcq_answer = MCQAnswer(
            text=toponymy_word.get_words(),
            is_true=is_true,
            explanation=toponymy_word.get_basic_description()
        )
        return mcq_answer



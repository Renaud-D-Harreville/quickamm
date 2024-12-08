from qa.toponymy.models import ToponymyWord, ToponymyList
from qa.models.models import MCQAnswer
from qa.mcq import AbstractMCQFactory
import random

class ToponymyToWordMCQFactory(AbstractMCQFactory):
    TOPICS = ["AMM", "AMM/Toponymie/Toponyme vers traduction"]

    def __init__(self, toponymy: ToponymyList):
        self.toponymy: ToponymyList = toponymy

    @property
    def topics(self):
        return self.TOPICS

    def _topic_weight(self, topic: str) -> int:
        return len(self.toponymy.words)

    def related_topics(self, surrounding_mcq_object: ToponymyWord) -> list[str]:
        return self.TOPICS

    def get_question(self, surrounding_mcq_object: ToponymyWord) -> str:
        question = f"Que signifient ces mots : {surrounding_mcq_object.get_words()}"
        return question

    def get_random_surrounding_question_object(self, topic: str) -> ToponymyWord:
        return random.choice(self.toponymy.words)

    def _to_mcq_answer(self, toponymy_word: ToponymyWord, is_true: bool) -> MCQAnswer:
        mcq_answer = MCQAnswer(
            text=toponymy_word.get_str_traduction(),
            is_true=is_true,
            description=toponymy_word.get_basic_description()
        )
        return mcq_answer

    def get_answers(self, surrounding_mcq_object: ToponymyWord) -> list[MCQAnswer]:
        correct_answer = self.get_true_answer(surrounding_mcq_object)
        wrong_answers = self.get_possible_false_answers(surrounding_mcq_object)
        answers = [correct_answer] + wrong_answers
        return answers

    def get_true_answer(self, surrounding_mcq_object: ToponymyWord) -> MCQAnswer:
        return self._to_mcq_answer(surrounding_mcq_object, True)

    def get_possible_false_answers(self, surrounding_mcq_object: ToponymyWord) -> list[str]:
        answers = [self._to_mcq_answer(word, False) for word in self.toponymy.words
                   if surrounding_mcq_object != word]
        return answers


class WordToToponymyMCQFactory(AbstractMCQFactory):
    TOPICS = ["AMM", "AMM/Toponymie/Traduction vers toponyme"]

    def __init__(self, toponymy: ToponymyList):
        self.toponymy: ToponymyList = toponymy

    @property
    def topics(self):
        return self.TOPICS

    def _topic_weight(self, topic: str) -> int:
        return len(self.toponymy.words)

    def related_topics(self, surrounding_mcq_object: ToponymyWord) -> list[str]:
        return self.TOPICS

    def get_question(self, surrounding_mcq_object: ToponymyWord) -> str:
        question = f"Quelle sont les toponymes possibles de : {surrounding_mcq_object.get_str_traduction()}"
        return question

    def get_random_surrounding_question_object(self, topic: str) -> ToponymyWord:
        return random.choice(self.toponymy.words)

    def _to_mcq_answer(self, toponymy_word: ToponymyWord, is_true: bool) -> MCQAnswer:
        mcq_answer = MCQAnswer(
            text=toponymy_word.get_words(),
            is_true=is_true,
            description=toponymy_word.get_basic_description()
        )
        return mcq_answer

    def get_answers(self, surrounding_mcq_object: ToponymyWord) -> list[MCQAnswer]:
        correct_answer = self.get_true_answer(surrounding_mcq_object)
        wrong_answers = self.get_possible_false_answers(surrounding_mcq_object)
        answers = [correct_answer] + wrong_answers
        return answers

    def get_true_answer(self, surrounding_mcq_object: ToponymyWord) -> MCQAnswer:
        return self._to_mcq_answer(surrounding_mcq_object, True)

    def get_possible_false_answers(self, surrounding_mcq_object: ToponymyWord) -> list[str]:
        answers = [self._to_mcq_answer(word, False) for word in self.toponymy.words
                   if surrounding_mcq_object != word]
        return answers

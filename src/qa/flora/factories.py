
from qa.mcq import AbstractMCQFactory
from pathlib import Path
import random

from qa.models.models import MCQAnswer
from qa.flora.models import Flowers, Flower




class FlowersMCQFactory(AbstractMCQFactory):
    TOPICS = ["AMM", "AMM/Flora"]

    def __init__(self, flowers: Flowers):
        self.flowers: Flowers = flowers

    @property
    def topics(self):
        return self.TOPICS

    def _topic_weight(self, topic: str) -> int:
        return len(self.flowers.flowers)

    def related_topics(self, surrounding_mcq_object: Flower) -> list[str]:
        return self.TOPICS

    def get_question(self, surrounding_mcq_object: Flower) -> str:
        question = "Quel est le nom de cette plante ?"
        return question

    def get_image_path(self, surrounding_mcq_object: Flower) -> Path | str | None:
        flower_picture_name = random.choice(surrounding_mcq_object.images_name)
        flower_picture_path = f"qcm/flora/{flower_picture_name}"
        return flower_picture_path

    def get_random_surrounding_question_object(self, topic: str) -> Flowers:
        return random.choice(self.flowers.flowers)

    @staticmethod
    def _to_mcq_answer(flower: Flower, is_true: bool) -> MCQAnswer:
        mcq_answer = MCQAnswer(
            text=flower.name,
            is_true=is_true,
            description=flower.description
        )
        return mcq_answer

    def get_answers(self, surrounding_mcq_object: Flower) -> list[MCQAnswer]:
        correct_answer = self.get_true_answer(surrounding_mcq_object)
        wrong_answers = self.get_possible_false_answers(surrounding_mcq_object)
        answers = [correct_answer] + wrong_answers
        return answers

    def get_true_answer(self, surrounding_mcq_object: Flower) -> MCQAnswer:
        return self._to_mcq_answer(surrounding_mcq_object, True)

    def get_possible_false_answers(self, surrounding_mcq_object: Flower) -> list[MCQAnswer]:
        answers = [self._to_mcq_answer(flower, False) for flower in self.flowers.flowers
                   if flower.name != surrounding_mcq_object.name]
        return answers
from qa.common.base_factory import AbstractMCQFactory
from pathlib import Path
import random
from qa.mcq_db.models import MCQAnswer
from qa.fauna.models import Animal, Animals


class AnimalsMCQFactory(AbstractMCQFactory):

    TOPICS = ["AMM", "Probatoire AMM", "Fauna"]

    def __init__(self, animals: Animals):
        self.animals: Animals = animals

    def get_questions_with_topics(self, topics: list[str]) -> list[Animal]:
        if all([topic in self.TOPICS for topic in topics]):
            return self.animals.animals
        return list()

    def get_question(self, surrounding_mcq_object: Animal) -> str:
        question = "Quel est le nom de cet animal ?"
        return question

    def get_image_path(self, surrounding_mcq_object: Animal) -> Path | str | None:
        animal_picture_name = random.choice(surrounding_mcq_object.images_name)
        animal_picture_path = f"qcm/fauna/{animal_picture_name}"
        return animal_picture_path

    def _to_mcq_answer(self, animal: Animal, is_true: bool) -> MCQAnswer:
        mcq_answer = MCQAnswer(
            text=animal.name,
            is_true=is_true,
            explanation=animal.description
        )
        return mcq_answer

    def get_answers(self, surrounding_mcq_object: Animal) -> list[MCQAnswer]:
        correct_answer = self.get_true_answer(surrounding_mcq_object)
        wrong_answers = self.get_possible_false_answers(surrounding_mcq_object)
        answers = [correct_answer] + wrong_answers
        return answers

    def get_true_answer(self, surrounding_mcq_object: Animal) -> MCQAnswer:
        return self._to_mcq_answer(surrounding_mcq_object, True)

    def get_possible_false_answers(self, surrounding_mcq_object: Animal) -> list[MCQAnswer]:
        answers = [self._to_mcq_answer(animal, False) for animal in self.animals.animals
                   if animal.name != surrounding_mcq_object.name]
        return answers

    def get_explanation(self, surrounding_mcq_object: Animal) -> str | None:
        return surrounding_mcq_object.description

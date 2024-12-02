from pydantic import BaseModel
from qa.mcq import AbstractMCQFactory
from qa import resource_dir_path
import json
from pathlib import Path
import random

fauna_json_path = resource_dir_path / "fauna/fauna.json"


class Animal(BaseModel):
    name: str
    images_name: list[str]
    description: str = ""


class Animals(BaseModel):
    animals: list[Animal]


class AnimalsMCQFactory(AbstractMCQFactory):
    TOPICS = ["AMM", "AMM/Fauna"]

    def __init__(self, animals: Animals):
        self.animals: Animals = animals

    @property
    def topics(self):
        return self.TOPICS

    def _topic_weight(self, topic: str) -> int:
        return len(self.animals.animals)

    def related_topics(self, surrounding_mcq_object: Animal) -> list[str]:
        return self.TOPICS

    def get_question(self, surrounding_mcq_object: Animal) -> str:
        question = "Quel est le nom de cet animal ?"
        return question

    def get_image_path(self, surrounding_mcq_object: Animal) -> Path | str | None:
        animal_picture_name = random.choice(surrounding_mcq_object.images_name)
        animal_picture_path = f"qcm/fauna/{animal_picture_name}"
        return animal_picture_path

    def get_random_surrounding_question_object(self, topic: str) -> Animal:
        return random.choice(self.animals.animals)

    def get_possible_true_answers(self, surrounding_mcq_object: Animal) -> list[str]:
        return [surrounding_mcq_object.name]

    def get_possible_false_answers(self, surrounding_mcq_object: Animal) -> list[str]:
        answers = [animal.name for animal in self.animals.animals]
        for true_answer in self.get_possible_true_answers(surrounding_mcq_object):
            answers.remove(true_answer)
        return answers


def get_animals() -> Animals:
    with open(fauna_json_path, "r", encoding='utf-8') as f:
        json_data = json.loads(f.read())
    return Animals(**json_data)


def save_animals(animals: Animals):
    json_model = animals.dict()
    with open(fauna_json_path, "w") as f:
        f.write(json.dumps(json_model, indent=2, ensure_ascii=False))

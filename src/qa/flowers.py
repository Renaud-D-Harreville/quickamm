from pydantic import BaseModel
from qa.mcq import MultipleChoiceQuestion, AbstractMCQFactory
from qa import resource_dir_path
import json
from pathlib import Path
import random

flowers_json_path = resource_dir_path / "flora/flowers.json"


class Flower(BaseModel):
    name: str
    images_name: list[str]
    description: str = ""


class Flowers(BaseModel):
    flowers: list[Flower]


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

    def get_possible_true_answers(self, surrounding_mcq_object: Flower) -> list[str]:
        return [surrounding_mcq_object.name]

    def get_possible_false_answers(self, surrounding_mcq_object: Flower) -> list[str]:
        answers = [flower.name for flower in self.flowers.flowers]
        for true_answer in self.get_possible_true_answers(surrounding_mcq_object):
            answers.remove(true_answer)
        return answers


def get_flowers() -> Flowers:
    with open(flowers_json_path, "r", encoding='utf-8') as f:
        json_data = json.loads(f.read())
    return Flowers(**json_data)


def save_flowers(flowers: Flowers):
    json_model = flowers.dict()
    with open(flowers_json_path, "w") as f:
        f.write(json.dumps(json_model, indent=2, ensure_ascii=False))

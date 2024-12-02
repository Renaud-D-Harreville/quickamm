from pydantic import BaseModel
from qa import resource_dir_path
from qa.mcq import AbstractMCQFactory
import json
import random

toponymy_json_path = resource_dir_path / "toponymy/toponymy.json"


class ToponymyWord(BaseModel):
    patois: list[str]
    traductions: list[str]

    def list_as_str(self, l: list) -> str:
        without_brackets = str(l)[1:-1]  # remove brackets
        without_quote = without_brackets.replace("'", "").replace('"', '')  # remove quotes
        return without_quote

    def get_str_traduction(self) -> str:
        return self.list_as_str(self.traductions)

    def get_words(self, max_words: int = 2):
        if max_words == -1 or max_words > len(self.patois):
            max_words = len(self.patois)
        words_list = random.sample(self.patois, k=max_words)
        return self.list_as_str(words_list)


class Toponymy(BaseModel):

    words: list[ToponymyWord]


class ToponymyMCQFactory(AbstractMCQFactory):
    TOPICS = ["AMM", "AMM/Toponymie"]

    def __init__(self, toponymy: Toponymy):
        self.toponymy: Toponymy = toponymy

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

    def get_possible_true_answers(self, surrounding_mcq_object: ToponymyWord) -> list[str]:
        return [surrounding_mcq_object.get_str_traduction()]

    def get_possible_false_answers(self, surrounding_mcq_object: ToponymyWord) -> list[str]:
        answers = [word.get_str_traduction() for word in self.toponymy.words]
        for true_answer in self.get_possible_true_answers(surrounding_mcq_object):
            answers.remove(true_answer)
        return answers


def get_toponymy() -> Toponymy:
    with open(toponymy_json_path, "r", encoding='utf-8') as f:
        json_data = json.loads(f.read())
    return Toponymy(**json_data)


def save_toponymy(toponymy: Toponymy):
    json_model = toponymy.dict()
    with open(toponymy_json_path, "w") as f:
        f.write(json.dumps(json_model, indent=2, ensure_ascii=False))

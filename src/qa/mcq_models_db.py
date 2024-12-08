import json
import random
from pathlib import Path
from pydantic import BaseModel
from qa import resource_dir_path
from qa.mcq import AbstractMCQFactory
from qa.models.models import MCQAnswer, MCQData

knowledge_json_path = resource_dir_path / "knowledge.json"
questions_json_path = resource_dir_path / "new_mcq_data.json"


class _SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MCQModelsDB(BaseModel):
    mcq_models: list[MCQData]

    # TODO: improve that function
    def get_questions_with_topic(self, topics: list[str] = None) -> list[MCQData]:
        if not topics:
            return self.mcq_models
        l = list()
        for question in self.mcq_models:
            for topic in topics:
                if question.is_under_topic(topic):
                    l.append(question)
                    break
        return l

    def get_random_question(self, topics: list[str] = None) -> MCQData:
        working_mcq_models = self.get_questions_with_topic(topics)
        random_mcq_model = random.choice(working_mcq_models)
        return random_mcq_model

    # TODO: To improve !
    def get_topic_list(self) -> list[str]:
        l = list()
        for question in self.mcq_models:
            l.extend(question.topics)
        return list(set(l))

    def add_question(self, question: MCQData):
        self.mcq_models.append(question)
        with open(questions_json_path, "wb") as f:
            f.write(self.json().encode("utf-8"))


class MCQDBMCQFactory(AbstractMCQFactory):

    def __init__(self, mcq_models_db: MCQModelsDB):
        self.mcq_models_db: MCQModelsDB = mcq_models_db

    @property
    def topics(self):
        return self.mcq_models_db.get_topic_list()

    def _topic_weight(self, topic: str) -> int:
        return len(self.mcq_models_db.get_questions_with_topic([topic]))

    def related_topics(self, surrounding_mcq_object: MCQData) -> list[str]:
        return surrounding_mcq_object.topics

    def get_question(self, surrounding_mcq_object: MCQData) -> str:
        return surrounding_mcq_object.question

    def get_image_path(self, surrounding_mcq_object: MCQData) -> Path | str | None:
        return surrounding_mcq_object.image_path

    def get_random_surrounding_question_object(self, topic: str) -> MCQData:
        return self.mcq_models_db.get_random_question([topic])

    def get_answers(self, surrounding_mcq_object: MCQData) -> list[MCQAnswer]:
        return surrounding_mcq_object.answers


with open(questions_json_path, "r", encoding='utf-8') as f:
    json_data = json.loads(f.read())
__question_db: MCQModelsDB = MCQModelsDB(**json_data)


def get_questions_db() -> MCQModelsDB:
    return __question_db
    # with open(questions_json_path, "r", encoding='utf-8') as f:
    #     json_data = json.loads(f.read())
    # return MCQModelsDB(**json_data)

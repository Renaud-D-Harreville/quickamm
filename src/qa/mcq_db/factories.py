from qa.mcq_db.models import MCQData, MCQAnswer, MCQModelsDB
from qa.api.base_factory import AbstractMCQFactory, SurroundingMCQObjectClass
from pathlib import Path

from qa.topics.themes import Theme


class MCQDBMCQFactory(AbstractMCQFactory):

    def __init__(self, mcq_models_db: MCQModelsDB):
        self.mcq_models_db: MCQModelsDB = mcq_models_db

    def get_questions_with_topics(self, topics: list[str]) -> list[SurroundingMCQObjectClass]:
        return self.mcq_models_db.get_questions_with_topics(topics)

    # @property
    # def topics(self):
    #     return self.mcq_models_db.get_topic_list()

    # def _topic_weight(self, topic: str) -> int:
    #     return len(self.mcq_models_db.get_questions_with_topic([topic]))
    #
    # def related_topics(self, surrounding_mcq_object: MCQData) -> list[str]:
    #     return surrounding_mcq_object.topics

    def get_question(self, surrounding_mcq_object: MCQData) -> str:
        return surrounding_mcq_object.question

    def get_image_path(self, surrounding_mcq_object: MCQData) -> Path | str | None:
        return surrounding_mcq_object.image_path

    # def get_random_surrounding_question_object(self, topic: str) -> MCQData:
    #     return self.mcq_models_db.get_random_question([topic])

    def get_answers(self, surrounding_mcq_object: MCQData) -> list[MCQAnswer]:
        return surrounding_mcq_object.answers

    def get_explanation(self, surrounding_mcq_object: MCQData) -> str | None:
        return surrounding_mcq_object.description

    # def get_all_surrounding_objects(self, topic: str) -> list[MCQData]:
    #     if self.is_under_topic(topic) is False:
    #         raise ValueError(f"Topic {topic} not in {self.topics}")
    #     return self.mcq_models_db.get_questions_with_topic([topic])

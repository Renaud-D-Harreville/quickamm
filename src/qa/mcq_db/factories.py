from qa.mcq_db.models import MCQData, MCQAnswer, MCQModelsDB, Reference
from qa.common.base_factory import AbstractMCQFactory, SurroundingMCQObjectClass
from pathlib import Path


class MCQDBMCQFactory(AbstractMCQFactory):

    def __init__(self, mcq_models_db: MCQModelsDB):
        self.mcq_models_db: MCQModelsDB = mcq_models_db

    def get_questions_with_topics(self, topics: list[str]) -> list[SurroundingMCQObjectClass]:
        return self.mcq_models_db.get_questions_with_topics(topics)

    def get_question(self, surrounding_mcq_object: MCQData) -> str:
        return surrounding_mcq_object.question

    def get_image_path(self, surrounding_mcq_object: MCQData) -> Path | str | None:
        return surrounding_mcq_object.image_path

    def get_answers(self, surrounding_mcq_object: MCQData) -> list[MCQAnswer]:
        return surrounding_mcq_object.answers

    def get_explanation(self, surrounding_mcq_object: MCQData) -> str | None:
        return surrounding_mcq_object.description

    def get_references(self, surrounding_mcq_object: MCQData) -> list[Reference] | None:
        return surrounding_mcq_object.references

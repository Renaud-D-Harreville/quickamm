
from pydantic import BaseModel
import random
from qa.common.models import Reference


class MCQAnswer(BaseModel):
    text: str
    is_true: bool
    explanation: str | None = None


class MCQData(BaseModel):
    topics: list[str]
    question: str
    image_path: str | None = None
    answers: list[MCQAnswer]
    description: str | None = None
    references: list[Reference] | None = None

    @property
    def correct_answers(self) -> list[MCQAnswer]:
        return [answer for answer in self.answers if answer.is_true]

    @property
    def wrong_answers(self) -> list[MCQAnswer]:
        return [answer for answer in self.answers if not answer.is_true]


class MCQModelsDB(BaseModel):
    mcq_models: list[MCQData]

    def get_questions_with_topics(self, topics: list[str] = None) -> list[MCQData]:
        if not topics:
            return self.mcq_models
        l = list()
        for question in self.mcq_models:
            if all([topic in question.topics for topic in topics]):
                l.append(question)
        return l

    def get_random_question(self, topics: list[str] = None) -> MCQData:
        working_mcq_models = self.get_questions_with_topic(topics)
        random_mcq_model = random.choice(working_mcq_models)
        return random_mcq_model

    def get_topic_list(self) -> list[str]:
        l = list()
        for question in self.mcq_models:
            l.extend(question.topics)
        return list(set(l))

    # # TODO: See how fauna, flora or toponymy works, and change this so that it would be deleted !
    # def add_question(self, question: MCQData):
    #     self.mcq_models.append(question)
    #     with open(questions_json_path, "wb") as f:
    #         f.write(self.json().encode("utf-8"))

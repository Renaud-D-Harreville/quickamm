from abc import ABC

from pydantic import BaseModel
from pydantic import HttpUrl
import random


#############################
####  Reference classes  ####
#############################


class Reference(BaseModel, ABC):
    type: str


class HttpUrlReference(Reference):
    type: str = "url-http"
    url: HttpUrl


class NoteReference(Reference):
    type: str = "note"
    note: str


#################################
####  'Normal' MCQs classes  ####
#################################


class MCQAnswer(BaseModel):
    text: str
    is_true: bool
    explanation: str | None = None
    references: list[Reference] | None = None


class MCQData(BaseModel):
    topics: list[str]
    question: str
    image_path: str | None = None
    answers: list[MCQAnswer]
    description: str | None = None

    @property
    def correct_answers(self) -> list[MCQAnswer]:
        return [answer for answer in self.answers if answer.is_true]

    @property
    def wrong_answers(self) -> list[MCQAnswer]:
        return [answer for answer in self.answers if not answer.is_true]

    def is_under_topic(self, topic: str) -> bool:
        for t in self.topics:
            # Search if for example t "AMM/Level2/Level3" starts with input topic "AMM/Level2"
            if t.startswith(topic):
                return True
        return False


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

    # # TODO: See how fauna, flora or toponymy works, and change this so that it would be deleted !
    # def add_question(self, question: MCQData):
    #     self.mcq_models.append(question)
    #     with open(questions_json_path, "wb") as f:
    #         f.write(self.json().encode("utf-8"))

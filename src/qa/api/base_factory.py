from abc import ABC, abstractmethod
from pathlib import Path

from qa.mcq_db.models import MCQAnswer, MCQData
from typing import TypeVar


SurroundingMCQObjectClass: TypeVar = TypeVar("SurroundingMCQObjectClass")


class AbstractMCQFactory(ABC):

    @abstractmethod
    def _topic_weight(self, topic: str) -> int:
        pass

    def is_under_topic(self, topic: str) -> bool:
        for t in self.topics:
            # Search if for example t "AMM/Level2/Level3" starts with input topic "AMM/Level2"
            if t.startswith(topic):
                return True
        return False

    def topic_weight(self, topic: str) -> int:
        if not self.is_under_topic(topic):
            return 0
        return self._topic_weight(topic)

    @property
    @abstractmethod
    def topics(self):
        pass

    def get_all_level_topics(self) -> list[str]:
        all_level_topics = []
        for topic in self.topics:
            split_topic = topic.split('/')
            for i in range(len(split_topic)):
                sub_topic = "/".join(split_topic[:i+1])
                all_level_topics.append(sub_topic)
        return list(set(all_level_topics))

    @abstractmethod
    def related_topics(self, surrounding_mcq_object: SurroundingMCQObjectClass) -> list[str]:
        pass

    @abstractmethod
    def get_question(self, surrounding_mcq_object: SurroundingMCQObjectClass) -> str:
        pass

    def get_image_path(self, surrounding_mcq_object: SurroundingMCQObjectClass) -> Path | str | None:
        return None

    @abstractmethod
    def get_all_surrounding_objects(self, topic: str) -> list[SurroundingMCQObjectClass]:
        pass

    @abstractmethod
    def get_random_surrounding_question_object(self, topic: str) -> SurroundingMCQObjectClass:
        pass

    @abstractmethod
    def get_answers(self, surrounding_mcq_object: SurroundingMCQObjectClass) -> list[MCQAnswer]:
        pass

    @abstractmethod
    def get_explanation(self, surrounding_mcq_object: SurroundingMCQObjectClass) -> str | None:
        pass

    def get_whole_mcq_data(self, surrounding_mcq_object: SurroundingMCQObjectClass) -> MCQData:
        return MCQData(
            topics=self.related_topics(surrounding_mcq_object),
            question=self.get_question(surrounding_mcq_object),
            image_path=self.get_image_path(surrounding_mcq_object),
            answers=self.get_answers(surrounding_mcq_object),
            description=self.get_explanation(surrounding_mcq_object)
        )




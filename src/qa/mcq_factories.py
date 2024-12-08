import random

from qa.fauna import AnimalsMCQFactory, get_animals
from qa.flora import FlowersMCQFactory, get_flowers
from qa.toponymy import ToponymyToWordMCQFactory, WordToToponymyMCQFactory, get_toponymy
from qa.mcq_models_db import MCQDBMCQFactory, get_questions_db
from qa.mcq import AbstractMCQFactory
from qa.models.models import MCQData


class AllQuestionsFactory:

    def __init__(self):
        self.questions_factories: list[AbstractMCQFactory] = list()
        self.__fullfill_questions_factories()

    def __fullfill_questions_factories(self):
        self.questions_factories.append(MCQDBMCQFactory(get_questions_db()))
        self.questions_factories.append(ToponymyToWordMCQFactory(get_toponymy()))
        self.questions_factories.append(WordToToponymyMCQFactory(get_toponymy()))
        self.questions_factories.append(AnimalsMCQFactory(get_animals()))
        self.questions_factories.append(FlowersMCQFactory(get_flowers()))

    def get_random_question_from_topics(self, topics: list[str]) -> MCQData:
        random_topic = random.choice(topics)
        weighted_factories = [factory.topic_weight(random_topic) for factory in self.questions_factories]
        factory: AbstractMCQFactory = random.choices(self.questions_factories, weights=weighted_factories, k=1)[0]
        question = factory.make_random_mcq(random_topic)
        return question

    @property
    def topics(self) -> list[str]:
        topics = list(set(topic for factory in self.questions_factories for topic in factory.get_all_level_topics()))
        topics.sort()
        return topics

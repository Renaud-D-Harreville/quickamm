import random

from qa.fauna import AnimalsMCQFactory, get_animals
from qa.flora import FlowersMCQFactory, get_flowers
from qa.toponymy import ToponymyToWordMCQFactory, WordToToponymyMCQFactory, get_toponymy
from qa.mcq_db import MCQDBMCQFactory, get_questions_db
from qa.api.base_factory import AbstractMCQFactory
from qa.mcq_db.models import MCQData
from qa.api.builders import MCQBuilder


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

    def get_random_factory_from_topics(self, topic: str, seed: int | float | str = 1) -> AbstractMCQFactory:
        seed_random = random.Random(seed)
        weighted_factories = [factory.topic_weight(topic) for factory in self.questions_factories]
        factory: AbstractMCQFactory = seed_random.choices(self.questions_factories, weights=weighted_factories, k=1)[0]
        return factory

    def make_user_mcq_object(self, whole_mcq_object: MCQData) -> MCQData:
        builder = MCQBuilder(whole_mcq_object, max_nb_correct_answers=2, probs=[1, 1/6])
        mcq = builder.build_mcq()
        return mcq

    def get_random_user_question_from_factory(self, topic: str, factory: AbstractMCQFactory, seed: int | float | str = None) -> MCQData:
        seed_random = random.Random(seed)
        questions = factory.get_all_surrounding_objects(topic)
        question = seed_random.choice(questions)
        whole_mcq_model = factory.get_whole_mcq_data(question)
        user_question = self.make_user_mcq_object(whole_mcq_model)
        return user_question

    def get_random_question_from_topics(self, topics: list[str], seed: int | float | str = None) -> MCQData:
        seed_random = random.Random(seed)
        random_topic = seed_random.choice(topics)
        factory = self.get_random_factory_from_topics(random_topic, seed)
        user_question = self.get_random_user_question_from_factory(random_topic, factory, seed)
        return user_question


    @property
    def topics(self) -> list[str]:
        topics = list(set(topic for factory in self.questions_factories for topic in factory.get_all_level_topics()))
        topics.sort()
        return topics

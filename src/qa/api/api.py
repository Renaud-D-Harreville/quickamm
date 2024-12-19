from qa.api.mcq_factories import AllQuestionsFactory
from qa.mcq_db.models import MCQData

all_questions_factory: AllQuestionsFactory = AllQuestionsFactory()


def get_random_question_from_topics(topics: list[str], seed: int | float | str = None) -> MCQData:
    return all_questions_factory.get_random_question_from_topics(topics, seed)


from qa.api.mcq_factories import AllQuestionsFactory
from qa.mcq_db.models import MCQData
from qa.topics.themes import get_themes

themes = get_themes()
all_questions_factory: AllQuestionsFactory = AllQuestionsFactory()


def get_random_question_from_topics(topics: list[str], seed: int | float | str = None) -> MCQData:
    return all_questions_factory.get_random_question_from_topics(topics, seed)

def get_theme_from_path(id_path: list[str]):
    return themes.get_theme_from_path(id_path)

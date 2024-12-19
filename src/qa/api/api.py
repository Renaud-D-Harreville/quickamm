from qa.api.mcq_factories import AllQuestionsFactory
from qa.mcq_db.models import MCQData
from qa.topics.themes import get_themes, Theme

themes = get_themes()
all_questions_factory: AllQuestionsFactory = AllQuestionsFactory()


def get_random_question_from_topics(topics: list[str], seed: int | float | str = None) -> MCQData:
    return all_questions_factory.get_random_question_from_topics(topics, seed)

def get_theme_from_path(id_path: list[str]):
    return themes.get_theme_from_path(id_path)

def get_sub_theme(theme: Theme, identifier: str):
    if identifier == theme.identifier:
        if len(theme.id_path) == 1:  # if theme is already on top of the hierarchy
            return theme
        return get_theme_from_path(theme.id_path[:-1])  # We exclude the current identifier of the path

    if identifier not in theme.sub_themes:
        return theme
    return theme.sub_themes[identifier]
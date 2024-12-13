from .base_view import AbstractQuestionView, all_questions_factory

class QuestionView(AbstractQuestionView):

    def get_default_topic(self) -> str:
        return "AMM"

    def get_topic_list(self) -> list[str]:
        return all_questions_factory.topics
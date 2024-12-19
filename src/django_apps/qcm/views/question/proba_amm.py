from .base_view import AbstractQuestionView

class QuestionView(AbstractQuestionView):

    def get_default_topic(self) -> str:
        return "AMM"

    def get_topic_list(self) -> list[str]:
        return ["AMM"]
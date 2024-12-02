from qa.mcq import MultipleChoiceQuestion
import json


class IndexPostRequestFacade:

    def __init__(self, request):
        self._request = request
        self._data = request.POST

    @property
    def mcq(self) -> MultipleChoiceQuestion:
        question_dict = json.loads(self._data["question"])
        question = MultipleChoiceQuestion(**question_dict)
        return question

    def answer_indexes(self) -> list[int]:
        answer_indexes = [int(index) for index in self._data.getlist('text_answers')]
        return answer_indexes

    def get_small_response(self) -> str:
        if self.mcq.is_correct_answer(self.answer_indexes()):
            small_response = "Bonne réponse !"
        else:
            small_response = f"Mauvaise réponse !"
        return small_response



import random

from qa.mcq_db.models import MCQData
import numpy as np

class MCQBuilder:

    def __init__(self, data:MCQData, total_nb_answers: int = 4, max_nb_correct_answers: int = 1, probs: list[float] = None):
        self.base_data = data
        if max_nb_correct_answers > len(data.correct_answers):
            max_nb_correct_answers = len(data.correct_answers)
            probs = None
        if total_nb_answers < max_nb_correct_answers:
            print(f"Cannot set max_nb_correct_answers > total_nb_answers ({max_nb_correct_answers} > {total_nb_answers})")
            print("Setting max_nb_correct_answers to total_nb_answers")
            max_nb_correct_answers = total_nb_answers
            probs = None
        self.nb_correct_answers = self._get_nb_correct_answer(max_nb_correct_answers, probs)
        self.total_nb_answers = total_nb_answers

    def _get_nb_correct_answer(self, max_nb_correct_answers: int, probs: list[float] = None) -> int:
        if not probs:
            probs = [1  / max_nb_correct_answers for _ in range(max_nb_correct_answers)]
        choices = list(range(1, max_nb_correct_answers + 1))
        return random.choices(choices, weights=probs, k=1)[0]

    @property
    def nb_wrong_answers(self) -> int:
        return self.total_nb_answers - self.nb_correct_answers

    def is_data_ok(self) -> bool:
        if (len(self.base_data.wrong_answers) >= self.nb_wrong_answers and
                len(self.base_data.correct_answers) >= self.nb_correct_answers):
            return True
        return False

    def build_mcq(self) -> MCQData:
        if not self.is_data_ok():
            return self.base_data
            raise Exception("Cannot build MCQ. Data is not valid")
        true_answers = list(np.random.choice(self.base_data.correct_answers, size=self.nb_correct_answers, replace=False))
        wrong_answers = list(np.random.choice(self.base_data.wrong_answers, size=self.nb_wrong_answers, replace=False))
        answer_list = true_answers + wrong_answers
        random.shuffle(answer_list)
        return MCQData(
            topics=self.base_data.topics,
            question=self.base_data.question,
            image_path=self.base_data.image_path,
            answers=answer_list,
            description=self.base_data.description,
            references=self.base_data.references
        )


from pydantic import BaseModel


class MCQAnswer(BaseModel):
    text: str
    is_true: bool
    description: str | None = None
    sources: list[str] | None = None


class BasicMCQData(BaseModel):
    question: str
    image_path: str | None = None
    answers: list[MCQAnswer]
    description: str | None = None

    @property
    def correct_answers(self) -> list[MCQAnswer]:
        return [answer for answer in self.answers if answer.is_true]

    @property
    def wrong_answers(self) -> list[MCQAnswer]:
        return [answer for answer in self.answers if not answer.is_true]


class MCQData(BasicMCQData):
    topics: list[str]

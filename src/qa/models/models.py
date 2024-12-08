from pydantic import BaseModel


class MCQAnswer(BaseModel):
    text: str
    is_true: bool
    description: str | None = None
    sources: list[str] | None = None


class MCQData(BaseModel):
    topics: list[str]
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

    def is_under_topic(self, topic: str) -> bool:
        for t in self.topics:
            # Search if for example t "AMM/Level2/Level3" starts with input topic "AMM/Level2"
            if t.startswith(topic):
                return True
        return False



from pydantic import BaseModel
import abc


class AbstractReference(BaseModel, abc.ABC):
    reference_type: str

    @abc.abstractmethod
    def to_html(self) -> str:
        pass


class URLReference(AbstractReference):
    reference_type: str = "url"
    url: str
    description: str

    def to_html(self) -> str:
        return f"<a href=\"{self.url}\" target=\"_blank\" rel=\"noopener noreferrer\">{self.description}</a>"


class TextReference(AbstractReference):
    reference_type: str = "text"
    text: str

    def to_html(self) -> str:
        return self.text


Reference = URLReference | TextReference
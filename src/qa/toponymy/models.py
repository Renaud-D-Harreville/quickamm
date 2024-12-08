from pydantic import BaseModel
import random


class ToponymyWord(BaseModel):
    patois: list[str]
    traductions: list[str]

    def list_as_str(self, l: list) -> str:
        without_brackets = str(l)[1:-1]  # remove brackets
        without_quote = without_brackets.replace("'", "").replace('"', '')  # remove quotes
        return without_quote

    def get_str_traduction(self) -> str:
        return self.list_as_str(self.traductions)

    def get_words(self, max_words: int = 2):
        if max_words == -1 or max_words > len(self.patois):
            max_words = len(self.patois)
        words_list = random.sample(self.patois, k=max_words)
        return self.list_as_str(words_list)

    def get_basic_description(self) -> str:
        str_patois = self.list_as_str(self.patois)
        return f"{str_patois} veulent dire : {self.get_str_traduction()}"


class ToponymyList(BaseModel):
    words: list[ToponymyWord]


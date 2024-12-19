import abc
from qa import resource_dir_path
from pydantic import BaseModel
import json
from typing import Any


class Theme(BaseModel):
    identifier: str
    name: str  # Would be used on the form
    description: str
    needed_topics: list[str]
    _id_path: list[str] = None
    sub_themes: dict[str, "Theme"] | None = None

    def model_post_init(self, __context):
        if self._id_path is None:
            self._set_id_path()

    def _set_id_path(self, parent_path: list[str] = None):
        if parent_path is None:
            parent_path = []
        self._id_path = parent_path + [self.identifier]
        if self.sub_themes:
            for _, sub_theme in self.sub_themes.items():
                sub_theme._set_id_path(self._id_path)

    def is_valid(self, topics: list[str], meta_data: dict[str, Any]):
        # At least one constraint should be true
        return any(constraint.is_valid(topics, meta_data) for constraint in self.constraints)


class Themes(BaseModel):
    themes: dict[str, Theme]

    def get_theme_from_path(self, path: list[str]) -> Theme:
        current_theme = self.themes[path[0]]
        for identifier in path[1:]:
            current_theme = current_theme.sub_themes[identifier]
        return current_theme


fauna_json_path = resource_dir_path / "themes.json"


def get_themes() -> Themes:
    with open(fauna_json_path, "r", encoding='utf-8') as f:
        json_data = json.loads(f.read())
    return Themes(**json_data)
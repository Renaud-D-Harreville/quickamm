from qa.topics.themes import Theme, Themes
from qa import resource_dir_path
import json

fauna_json_path = resource_dir_path / "themes.json"


def get_themes() -> Themes:
    with open(fauna_json_path, "r", encoding='utf-8') as f:
        json_data = json.loads(f.read())
    return Themes(**json_data)

class TestThemes:
    def test_create(self):
        themes = get_themes()
        path = ["Probatoire AMM", "Milieu montagnard"]
        sub_theme = themes.get_theme_from_path(path)
        assert sub_theme.name == "Milieu montagnard"
        assert sub_theme._id_path == path

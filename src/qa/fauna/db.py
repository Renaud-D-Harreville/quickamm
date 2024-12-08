from qa.fauna.models import Animals
from qa import resource_dir_path
import json

fauna_json_path = resource_dir_path / "fauna/fauna.json"


def get_animals() -> Animals:
    with open(fauna_json_path, "r", encoding='utf-8') as f:
        json_data = json.loads(f.read())
    return Animals(**json_data)


def save_animals(animals: Animals):
    json_model = animals.dict()
    with open(fauna_json_path, "w") as f:
        f.write(json.dumps(json_model, indent=2, ensure_ascii=False))

from qa.toponymy.models import ToponymyList
from qa import resource_dir_path
import json

toponymy_json_path = resource_dir_path / "toponymy/toponymy.json"


def get_toponymy() -> ToponymyList:
    with open(toponymy_json_path, "r", encoding='utf-8') as f:
        json_data = json.loads(f.read())
    return ToponymyList(**json_data)


def save_toponymy(toponymy: ToponymyList):
    json_model = toponymy.dict()
    with open(toponymy_json_path, "w") as f:
        f.write(json.dumps(json_model, indent=2, ensure_ascii=False))

from qa.flora.models import Flowers
from qa import resource_dir_path
import json


flowers_json_path = resource_dir_path / "flora/flowers.json"






def get_flowers() -> Flowers:
    with open(flowers_json_path, "r", encoding='utf-8') as f:
        json_data = json.loads(f.read())
    return Flowers(**json_data)


def save_flowers(flowers: Flowers):
    json_model = flowers.dict()
    with open(flowers_json_path, "w") as f:
        f.write(json.dumps(json_model, indent=2, ensure_ascii=False))

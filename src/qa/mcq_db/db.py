import json
from qa import resource_dir_path
from qa.mcq_db.models import MCQModelsDB
# knowledge_json_path = resource_dir_path / "knowledge.json"
questions_json_path = resource_dir_path / "mcq_explanation.json"


class _SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]





with open(questions_json_path, "r", encoding='utf-8') as f:
    json_data = json.loads(f.read())
__question_db: MCQModelsDB = MCQModelsDB(**json_data)


def get_questions_db() -> MCQModelsDB:
    return __question_db
    # with open(questions_json_path, "r", encoding='utf-8') as f:
    #     json_data = json.loads(f.read())
    # return MCQModelsDB(**json_data)
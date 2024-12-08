from pydantic import BaseModel


class Flower(BaseModel):
    name: str
    images_name: list[str]
    description: str = ""


class Flowers(BaseModel):
    flowers: list[Flower]

from pydantic import BaseModel


class Animal(BaseModel):
    name: str
    images_name: list[str]
    description: str = ""


class Animals(BaseModel):
    animals: list[Animal]
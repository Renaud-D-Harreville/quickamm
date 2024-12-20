from pydantic import BaseModel
from qa.common.models import Reference


class SpeciesImage(BaseModel):
    static_path: str
    short_description: str
    references: list[Reference] | None = None


class Classification(BaseModel):
    order: str | None = None
    family: str | None = None
    genus: str | None = None
    species: str | None = None

class OneSpecies(BaseModel):
    french_name: str
    latin_name: str
    description: str = ""
    images: list[SpeciesImage] | None = None
    classification: Classification | None = None
    references: list[Reference] | None = None

    def get_classification_topics(self) -> list[str]:
        return [
            f"order:{self.classification.order}",
            f"family:{self.classification.family}",
            f"genus:{self.classification.genus}",
            f"species:{self.classification.species}"
        ]


class AllSpecies(BaseModel):
    species: dict[str, OneSpecies]  # Key should be the latin name of the species


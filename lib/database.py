import json
from enum import Enum
from typing import Any, Self
from pprint import pprint
from dataclasses import dataclass

from jsonschema import validate, Draft202012Validator
from haystack.dataclasses import Document

class LocationType(Enum):
    LOCAL = "local"
    WEBSITE = "website"

# Desc
index_schema = {
    "type": "object",
    "patternProperties": {
        "^.*$": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "location": {
                        "type": "string"
                    },
                    "location_type": {
                        "enum": [location_type.value for location_type in LocationType]
                    }
                },
                "required": [
                    "keywords",
                    "location",
                    "location_type"
                ],
                "additionalProperties": False
            }
        }
    },
    "additionalProperties": False
}

@dataclass(slots = True)
class Link:
    """
    Represents a link between a collection of keywords and a file containing some text.
    """

    keywords: list[str]
    location: str
    type: LocationType

    def read_document(self) -> Document:
        match self.type:
            case LocationType.LOCAL:
                with open(self.location, "r") as file:
                    return Document(
                        id = self.location,
                        content = file.read()
                    )
            case LocationType.WEBSITE:
                raise NotImplemented()
            case _:
                assert False, "Unreachable"

    def match_keywords(self, text: str) -> bool:
        return any(word in self.keywords for word in text.split())


@dataclass(slots = True)
class Subject:
    name: str
    links: list[Link]

    @classmethod
    def from_links(cls, name: str, data: list[dict[str, str | list]]) -> Self:
        links: list[Link] = []
        for link in data:
            links.append(Link(link["keywords"], link["location"], LocationType(link["location_type"])))
        self = object.__new__(cls)
        self.__init__(name, links)
        return self

class Database:
    def __init__(self, index_path: str) -> None:
        self.index_path: str = index_path
        self.data: list[Subject] = []
        self.update_data()

    def update_data(self) -> None:
        with open(self.index_path, "r") as file:
            index_data: dict[str, list] = json.load(file)

        if not self.verify_data(index_data):
            return

        self.data = [
            Subject.from_links(subject_name, links)
            for subject_name, links in index_data.items()
        ]

    @staticmethod
    def verify_data(data: dict) -> bool:
        Draft202012Validator.check_schema(index_schema)
        validator = Draft202012Validator(index_schema)
        return validator.is_valid(data)

    def fetch_relevant_documents(self, subject_name: str, text: str) -> list[Document]:
        for subject in self.data:
            if subject.name == subject_name:
                result: list[Document] = []
                for link in subject.links:
                    if link.match_keywords(text):
                        result.append(link.read_document())
                return result
        else:
            raise ValueError(f"{subject_name} is not a valid subject name.")



db = Database("../data/index.json")

print(db.fetch_relevant_documents("Programmering 2", "Tell me how to make a class in java."))
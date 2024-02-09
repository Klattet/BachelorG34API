import json
from enum import Enum
from typing import Any, Self
from pprint import pprint
from dataclasses import dataclass

import jsonschema
from jsonschema import validate, Draft202012Validator

class LocationType(Enum):
    LOCAL = "local"
    WEBSITE = "website"

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
    }
}

@dataclass(slots = True)
class Link:
    keywords: list[str]
    location: str
    type: LocationType

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




db = Database("../data/index.json")


from typing import List, Optional

from fastapi import FastAPI

from fastapi_hypermodel import HyperModel, HyperRef


class ItemSummary(HyperModel):
    name: str
    id: str
    href: HyperRef

    class Href:
        endpoint = "read_item"
        values = {"item_id": "<id>"}


class Item(ItemSummary):
    description: Optional[str] = None
    price: float


class Person(HyperModel):
    name: str
    id: str
    items: List[ItemSummary]
    href: HyperRef

    class Href:
        endpoint = "read_person"
        values = {"person_id": "<id>"}


items = {
    "item01": {"id": "item01", "name": "Foo", "price": 50.2},
    "item02": {
        "id": "item02",
        "name": "Bar",
        "description": "The Bar fighters",
        "price": 62,
    },
    "item03": {
        "id": "item03",
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
    },
}

people = {
    "person01": {
        "id": "person01",
        "name": "Alice",
        "items": [items["item01"], items["item02"]],
    },
    "person02": {"id": "person02", "name": "Bob", "items": [items["item03"]]},
}


def create_app():
    app = FastAPI()
    HyperModel.init_app(app)

    @app.get(
        "/items",
        response_model=List[ItemSummary],
    )
    def read_items():
        return list(items.values())

    @app.get("/items/{item_id}", response_model=Item)
    def read_item(item_id: str):
        return items[item_id]

    @app.get(
        "/people",
        response_model=List[Person],
    )
    def read_people():
        return list(people.values())

    @app.get("/people/{person_id}", response_model=Person)
    def read_person(person_id: str):
        return people[person_id]

    return app

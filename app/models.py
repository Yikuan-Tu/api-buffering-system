# app/models.py for type validation
from typing import List
from pydantic import BaseModel, RootModel

class Person(BaseModel):
    first_name: str
    last_name: str

class SubmitRequest(RootModel):
    root: List[Person]

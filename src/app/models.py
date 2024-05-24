from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    kind: str


class Filters(BaseModel):
    author: list[str] | None = None
    kind: list[str] | None = None

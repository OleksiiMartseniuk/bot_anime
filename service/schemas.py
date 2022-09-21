from pydantic import BaseModel


class Names(BaseModel):
    ru: str
    en: str


class Posters(BaseModel):
    small: str
    medium: str
    original: str


class PType(BaseModel):
    full_string: str
    string: str
    series: int | None
    length: str


class AnimeAniLibria(BaseModel):
    id: int
    code: str
    names: Names
    posters: Posters
    updated: int
    last_change: int
    type: PType
    genres: list[str]
    description: str

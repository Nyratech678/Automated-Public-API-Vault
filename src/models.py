from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class API:
    name: str
    description: str
    topics: list[str]
    url: str
    stars: int
    language: Optional[str] = None
    license: Optional[str] = None
    updated_at: Optional[str] = None
    archived: bool = False
    homepage: Optional[str] = None
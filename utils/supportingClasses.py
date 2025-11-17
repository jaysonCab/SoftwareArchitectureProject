from dataclasses import dataclass, field

@dataclass
class User:
    id: int
    username: str
    watched_shows: list = field(default_factory=list)  # will fill later from DB

@dataclass
class Show:
    id: int
    user_id: int
    show_name: str
    personal_score: int
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TextData:
    source: str
    id: str
    content: str
    created_at: datetime
    intention: str


@dataclass
class Source:
    id: str
    title: str


@dataclass
class Intention:
    id: str
    title: str


@dataclass
class Tag:
    id: int
    title: str


@dataclass
class Query:
    id: int
    query: str


@dataclass
class Label:
    tag: Tag
    text_data: TextData
    timestamp: datetime


@dataclass
class AlreadyLabeled:
    query: Query
    text_data: TextData
    timestamp: datetime


@dataclass
class Statistics:
    text_data: int
    already_labeled: int
    matches: int

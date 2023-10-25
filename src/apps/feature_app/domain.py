import abc
from dataclasses import dataclass
from datetime import datetime


class BaseRedisRepository(abc.ABC):
    @abc.abstractmethod
    def get_conn(self): ...


@dataclass
class User:
    id: int


@dataclass
class Article:
    title: str
    link: str
    user: User
    time: datetime
    votes: int


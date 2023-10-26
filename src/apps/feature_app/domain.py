import abc
from collections import namedtuple
from dataclasses import dataclass
from datetime import datetime


class BaseRedisRepository(abc.ABC):
    @abc.abstractmethod
    def get_conn(self): ...


WSGIRequest = namedtuple('WSGIRequest', 'user article group token item')

User = namedtuple('User', 'id')

Article = namedtuple('Article', 'id')

Group = namedtuple('Group', 'name')

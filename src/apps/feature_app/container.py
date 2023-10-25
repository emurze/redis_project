from collections import namedtuple

from .collection import commands
from .infrastructure import RedisRepository

WSGIRequest = namedtuple('WSGIRequest', 'user')
User = namedtuple('User', 'id')


class FeatureAppContainer:
    @staticmethod
    def get_commands() -> dict:
        redis_repository = RedisRepository()

        return {
            command: _Service(redis_repository)
            for command, _Service in commands.items()
        }

    @staticmethod
    def get_request() -> WSGIRequest:
        user = User(100)
        request = WSGIRequest(user)
        return request

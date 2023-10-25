import redis

from config import settings
from .domain import BaseRedisRepository


class RedisRepository(BaseRedisRepository):
    def __init__(self):
        self.redis = redis.Redis(
            db=settings.REDIS_FEATURE_DB,
            port=settings.REDIS_FEATURE_PORT,
            host=settings.REDIS_FEATURE_HOST,
        )

    def get_conn(self):
        return self.redis

import time
import logging
from dataclasses import dataclass

from config import settings
from .domain import User, Article, Group, WSGIRequest
from .infrastructure import RedisRepository

lg = logging.getLogger(__name__)
ONE_WEEK_IN_SECONDS = 60 * 86400
VOTE_SCORE = 432  # if user didn't vote


@dataclass
class CreateArticleService:
    redis_repository: RedisRepository

    def run(self, request):
        conn = self.redis_repository.get_conn()
        article_id = conn.incr('article:')

        now = int(time.time())
        voted_table_name = f'voted:{article_id}'
        conn.sadd(voted_table_name, request.user.id)
        conn.expire(voted_table_name, ONE_WEEK_IN_SECONDS)

        article_table_name = f'article:{article_id}'
        conn.hmset(article_table_name, {
            'id': article_id,
            'title': f'Article_{article_id}',
            'link': '',
            'user_id': request.user.id,
            'time': now,
            'votes': 1,
        })

        conn.zadd('score:', {article_id: now + VOTE_SCORE})
        conn.zadd('time:', {article_id: now})


@dataclass
class VoteArticleService:
    redis_repository: RedisRepository

    def run(self, request):
        conn = self.redis_repository.get_conn()
        now = int(time.time())
        two_weeks = now - ONE_WEEK_IN_SECONDS

        # Stop if Article doesn't exist
        if not conn.hgetall(f'article:{request.article.id}'):
            lg.warning("Operation stopped. Article doesn't exist")
            return

        # Stop if Article published more than 2 weeks ago
        if conn.zscore(f'time:', request.article.id) < two_weeks:
            lg.warning(
                "Operation stopped. Article created more than two weeks ago"
            )
            return

        # if successfully added then execution
        if conn.sadd(f'voted:{request.article.id}', request.user.id):
            conn.zincrby(f'score:', request.article.id, 300)
            conn.hmset(f'article:{request.article.id}', {'votes': 2})


@dataclass
class GetArticlesService:
    redis_repository: RedisRepository

    def run(self, request, order='score:'):
        conn = self.redis_repository.get_conn()

        article_ids = conn.zrevrange(order, 0, -1)
        articles = [
            {
                k.decode(settings.ENCODING): v.decode(settings.ENCODING)
                for k, v in conn.hgetall(f'article:{article_id}').items()
            }
            for article_id in map(lambda x: x.decode('utf-8'), article_ids)
        ]
        lg.warning(articles)


@dataclass
class AddItemToGroupService:
    redis_repository: RedisRepository

    def run(self, request):
        conn = self.redis_repository.get_conn()

        article_id = request.article.id
        group_name = request.group.name

        conn.sadd(f'group:{group_name}', article_id)

        lg.warning(conn.smembers(f'group:{group_name}'))


@dataclass
class RemoveItemFromGroupService:
    redis_repository: RedisRepository

    def run(self, request):
        conn = self.redis_repository.get_conn()

        article_id = request.article.id
        group_name = request.group.name

        conn.srem(f'group:{group_name}', article_id)


@dataclass
class DeleteAllArticles:
    redis_repository: RedisRepository

    def run(self, request):
        conn = self.redis_repository.get_conn()

        conn.delete(*[f'article:{article_id}'
                      for article_id in range(1, 101)])


@dataclass
class GetToken:
    redis_repository: RedisRepository

    def run(self, request):
        conn = self.redis_repository.get_conn()
        return conn.hget('login:', request.token)


@dataclass
class UpdateToken:
    redis_repository: RedisRepository

    def run(self, request):
        conn = self.redis_repository.get_conn()

        timestamp = int(time.time())
        conn.hset('login:', request.token, request.user.id)
        conn.zadd('recent:', {request.token: timestamp})

        if request.item:
            conn.zadd(f'viewed:{request.token}', {request.item: timestamp})
            conn.zremrangebyrank(f'viewed:{request.token}', 0, -25)
            # remain only last 25 viewed items


LIMIT = 100


@dataclass
class CleanSession:
    redis_repository: RedisRepository

    def run(self, request):
        conn = self.redis_repository.get_conn()

        size = conn.zcard('recent:')
        if size <= LIMIT:
            return

        tokens = conn.zrange('recent', 0, -50)
        session_keys = [f'viewed:{token}' for token in tokens]
        conn.delete(*session_keys)
        conn.hdel('login:', *tokens)
        conn.zrem('recent:', *tokens)


class FeatureFactory:
    @staticmethod
    def get_user(_id) -> User:
        return User(_id)

    @staticmethod
    def get_article(_id) -> Article:
        return Article(_id)

    @staticmethod
    def get_group(name) -> Group:
        return Group(name)

    @staticmethod
    def get_request(**options) -> WSGIRequest:
        return WSGIRequest(**options)

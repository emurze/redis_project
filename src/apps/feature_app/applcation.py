import time
import logging
from dataclasses import dataclass

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

    def run(self):
        pass

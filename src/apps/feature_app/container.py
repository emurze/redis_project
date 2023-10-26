import logging

from .applcation import FeatureFactory
from .collection import commands
from .infrastructure import RedisRepository

lg = logging.getLogger(__name__)


class FeatureAppContainer:
    user_id = 143
    article_id = 32
    group_name = 'track'
    token = 'wefwefwdfq32rfq3wfdqdf'
    item = 'great_post_31'

    @staticmethod
    def get_commands() -> dict:
        redis_repository = RedisRepository()

        return {
            command: _Service(redis_repository)
            for command, _Service in commands.items()
        }

    def get_request(self):
        user = FeatureFactory.get_user(self.user_id)
        article = FeatureFactory.get_article(self.user_id)
        group = FeatureFactory.get_group(self.group_name)
        request = FeatureFactory.get_request(
            user=user,
            article=article,
            group=group,
            token=self.token,
            item=self.item,
        )
        return request

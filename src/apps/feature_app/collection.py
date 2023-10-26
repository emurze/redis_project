from .applcation import (
    CreateArticleService,
    VoteArticleService,
    GetArticlesService, RemoveItemFromGroupService, AddItemToGroupService,
    DeleteAllArticles, GetToken, UpdateToken,
)

commands = {
    'create_article': CreateArticleService,
    'vote_article': VoteArticleService,
    'get_articles': GetArticlesService,
    'add_item_to_group': AddItemToGroupService,
    'delete_all_articles': DeleteAllArticles,
    'remove_article_from_group': RemoveItemFromGroupService,

    'get_token': GetToken,
    'update_token': UpdateToken,
}

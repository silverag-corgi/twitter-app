from typing import Final

TWITTER_API_AUTH_INFO_PATH: Final[str] = 'config/twitter_api_auth_info.json'

FOLLOWEE_TWITTER_LIST_NAME: Final[str] = 'followee_{0}_{1}'
FOLLOWER_TWITTER_LIST_NAME: Final[str] = 'follower_{0}_{1}'

TWITTER_LIST_FILE_PATH: Final[str] = \
    './dest/twitter_list/{0}.csv'
TWITTER_TWEET_SEARCH_RESULT_FILE_PATH: Final[str] = \
    './dest/tweet_search_result/{0}.csv'

TWITTER_LISTS_HEADER: Final[list[str]] = \
    [
        'creation_datetime',
        'twitter_list_id',
        'twitter_list_name',
        'num_of_members',
    ]
TWITTER_LIST_HEADER: Final[list[str]] = \
    [
        'twitter_user_id',
        'twitter_user_name',
        'url',
    ]
TWITTER_TWEET_SEARCH_RESULT_HEADER: Final[list[str]] = \
    [
        'creation_datetime',
        'twitter_user_id',
        'twitter_user_name',
        'tweet_text',
        'retweet_count',
        'favorite_count',
        'url',
    ]

TWITTER_ACCOUNT_URL: Final[str] = \
    'https://twitter.com/{0}'
TWITTER_TWEET_URL: Final[str] = \
    'https://twitter.com/{0}/status/{1}'

ENCODING: Final[str] = 'utf8'

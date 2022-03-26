from typing import Final

TWITTER_API_AUTH_INFO_FILE_PATH: Final[str] = \
    'config/twitter_api_auth_info.json'

FOLLOWEE_LIST_NAME: Final[str] = \
    'followee_{0}_{1}'
FOLLOWER_LIST_NAME: Final[str] = \
    'follower_{0}_{1}'

LIST_MEMBER_FILE_PATH: Final[str] = \
    './dest/twitter_list/{0}.csv'
TWEET_SEARCH_RESULT_FILE_PATH: Final[str] = \
    './dest/tweet_search_result/{0}.csv'

LIST_HEADER: Final[list[str]] = \
    [
        'creation_datetime',
        'list_id',
        'list_name',
        'num_of_members',
    ]
LIST_MEMBER_HEADER: Final[list[str]] = \
    [
        'user_id',
        'user_name',
        'url',
    ]
TWEET_SEARCH_RESULT_HEADER: Final[list[str]] = \
    [
        'creation_datetime',
        'user_id',
        'user_name',
        'tweet_text',
        'retweet_count',
        'favorite_count',
        'url',
    ]

ACCOUNT_URL: Final[str] = \
    'https://twitter.com/{0}'
TWEET_URL: Final[str] = \
    'https://twitter.com/{0}/status/{1}'

ENCODING: Final[str] = 'utf8'

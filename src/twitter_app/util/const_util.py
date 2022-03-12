from typing import Final

TWITTER_API_AUTH_INFO_PATH: Final[str] = 'config/twitter_api_auth_info.json'

FOLLOWEE_TWITTER_LIST_NAME: Final[str] = 'followee_{0}_{1}'
FOLLOWER_TWITTER_LIST_NAME: Final[str] = 'follower_{0}_{1}'

TWITTER_TWEET_SEARCH_RESULT_FILE_PATH: Final[str] = \
    './dest/tweet_search_result/tweet_search_result_{0}.csv'

TWITTER_LIST_FILE_HEADER: Final[list[str]] = \
    [
        'user_id',
        'user_name',
    ]
TWITTER_TWEET_SEARCH_RESULT_HEADER: Final[list[str]] = \
    [
        'creation_datetime',
        'user_id',
        'user_name',
        'tweet_text',
        'retweet_count',
        'favorite_count',
        'url',
    ]

TWITTER_URL: Final[str] = 'https://twitter.com/{0}/status/{1}'

ENCODING: Final[str] = 'utf8'
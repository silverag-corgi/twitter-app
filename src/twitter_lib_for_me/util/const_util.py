from typing import Final

FOLLOWEE_TWITTER_LIST_NAME: Final[str] = 'followee_{0}_{1}'
FOLLOWER_TWITTER_LIST_NAME: Final[str] = 'follower_{0}_{1}'

TWITTER_TWEET_SEARCH_RESULT_FILE_PATH: Final[str] = \
    './dest/tweet_search_result/tweet_search_result_{0}.csv'

TWITTER_TWEET_SEARCH_RESULT_HEADER: Final[list[str]] = \
    [
        'created_datetime',
        'user_id',
        'user_name',
        'tweet_text',
        'retweet_count',
        'favorite_count',
        'url',
    ]

TWITTER_URL: Final[str] = 'https://twitter.com/{0}/status/{1}'

ENCODING: Final[str] = 'utf8'

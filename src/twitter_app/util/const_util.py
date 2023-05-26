from typing import Final

# fmt: off

TWITTER_API_AUTH_INFO_FILE_PATH: Final[str] = \
    "config/twitter_api_auth_info.json"

FOLLOWEE_FILE_PATH: Final[str] = \
    "./dest/followee/{0}_{1}.csv"
FOLLOWER_FILE_PATH: Final[str] = \
    "./dest/follower/{0}_{1}.csv"

LIST_MEMBER_FILE_PATH: Final[str] = \
    "./dest/list_member/{0}.csv"
TWEET_SEARCH_RESULT_FILE_PATH: Final[str] = \
    "./dest/tweet_search_result/{0}.csv"

LIST_HEADER: Final[list[str]] = \
    [
        "creation_datetime",
        "list_id",
        "list_name",
        "num_of_members",
    ]
LIST_MEMBER_HEADER: Final[list[str]] = \
    [
        "user_id",
        "user_name",
        "url",
    ]
TWEET_SEARCH_RESULT_HEADER: Final[list[str]] = \
    [
        "creation_datetime",
        "user_id",
        "user_name",
        "tweet_text",
        "retweet_count",
        "favorite_count",
        "url",
    ]

ACCOUNT_URL: Final[str] = \
    "https://twitter.com/{0}"
TWEET_URL: Final[str] = \
    "https://twitter.com/{0}/status/{1}"

ENCODING: Final[str] = "utf8"

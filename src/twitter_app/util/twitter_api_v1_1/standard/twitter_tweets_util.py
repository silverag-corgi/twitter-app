from enum import Enum, IntEnum
from logging import Logger
from typing import Any, Optional

import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet

from twitter_app.util import const_util


class SEARCH_RESULT_TYPE(Enum):
    MIXED = 'mixed'         # 最新の検索結果と人気のある検索結果
    RECENT = 'recent'       # 最新の検索結果のみ
    POPULAR = 'popular'     # 人気のある検索結果のみ


class TWEETS_IN_PAST_7DAY(IntEnum):
    MAX_NUM_OF_DATA_PER_REQUEST = 100
    MAX_NUM_OF_REQUESTS_PER_15MIN = 180


def search_tweets_in_past_7day(
        api: tweepy.API,
        query: str,
        search_result_type: SEARCH_RESULT_TYPE,
        num_of_data_per_request: int = TWEETS_IN_PAST_7DAY.MAX_NUM_OF_DATA_PER_REQUEST.value,
        num_of_requests: int = TWEETS_IN_PAST_7DAY.MAX_NUM_OF_REQUESTS_PER_15MIN.value
    ) -> list[ResultSet]:
    
    '''
    ツイート検索(過去7日間)
    
    Args:
        api (tweepy.API)                        : API
        query (str)                             : クエリ
        search_result_type (SEARCH_RESULT_TYPE) : 検索結果の種類
        num_of_data_per_request (int, optional) : リクエストごとのデータ数(デフォルト：100)
        num_of_requests (int, optional)         : リクエスト数(デフォルト：180)
    
    Returns:
        list[ResultSet] : ツイート検索結果ページ (list[ResultSet[tweepy.models.SearchResults]])
    
    Notes:
        - 使用するエンドポイントはGETメソッドである
        - 引数「リクエストごとのデータ数」は上限が100データ
            - 超過して指定した場合は上限で上書きする
        - 引数「リクエスト数」は15分ごとに最大180リクエスト
            - 超過して指定した場合はレート制限により15分の待機時間が発生する
        - 15分で最大18000データを取得できる
            - 100 data/req * 180 req/15-min = 18000 data/15-min
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets
            - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/guides/standard-operators
        - オブジェクトモデル
            - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    tweet_search_result_pages: list[ResultSet] = []
    
    try:
        lg = pyl.get_logger(__name__)
        
        pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
        
        tweet_search_result_pagination: tweepy.Cursor = tweepy.Cursor(
                api.search_tweets,
                q=query,
                result_type=search_result_type,
                count=num_of_data_per_request
                if (num_of_data_per_request <=
                    TWEETS_IN_PAST_7DAY.MAX_NUM_OF_DATA_PER_REQUEST.value)
                else TWEETS_IN_PAST_7DAY.MAX_NUM_OF_DATA_PER_REQUEST.value
            )
        tweet_search_result_pages = list(tweet_search_result_pagination.pages(num_of_requests))
        
        pyl.log_inf(lg, f'ツイート検索(過去7日間)に成功しました。(query:{query})')
    except Exception as e:
        if lg is not None:
            pyl.log_war(lg, f'ツイート検索(過去7日間)に失敗しました。(query:{query})', e)
    
    return tweet_search_result_pages


class CustomStream(tweepy.Stream):
    def on_status(self, tweet: Any) -> None:
        try:
            lg: Logger = pyl.get_logger(__name__)
            
            tweet.created_at = pyl.convert_timestamp_to_jst(str(tweet.created_at))
            tweet.text = str(tweet.text).replace('\n', '')
            tweet_url: str = const_util.TWITTER_TWEET_URL.format(tweet.user.screen_name, tweet.id)
            
            pyl.log_inf(lg, f'{tweet.created_at}, ' +
                            f'{tweet.user.screen_name: <15}, ' +
                            f'{tweet.user.name: <20}, ' +
                            f'{tweet.text}, ' +
                            f'{tweet_url}')
        except Exception as e:
            pass


class Stream(IntEnum):
    MAX_NUM_OF_KEYWORDS = 400
    MAX_NUM_OF_FOLLOWING = 5000


def stream_tweets(
        api: tweepy.API,
        following_user_ids: Optional[list[str]] = None,
        keywords: Optional[list[str]] = None
    ) -> None:
    
    '''
    ツイート配信
    
    Args:
        api (tweepy.API)                            : API
        following_user_ids (Optional[list[str]])    : フォローユーザID (×：TwitterユーザID、〇：ユーザID)
        keywords (Optional[list[str]])              : キーワード
    
    Returns:
        -
    
    Notes:
        - 使用するエンドポイントはPOSTメソッドである
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/filter-realtime/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/filter-realtime/api-reference/post-statuses-filter
            - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/filter-realtime/guides/basic-stream-parameters#follow
            - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/filter-realtime/guides/basic-stream-parameters#track
        - オブジェクトモデル
            - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        auth: Any = api.auth
        stream: CustomStream = CustomStream(
                auth.consumer_key,
                auth.consumer_secret,
                auth.access_token,
                auth.access_token_secret
            )
        
        stream.filter(follow=following_user_ids, track=keywords, languages=['ja'])
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'ツイート配信に失敗しました。')
        raise(e)
    
    return None

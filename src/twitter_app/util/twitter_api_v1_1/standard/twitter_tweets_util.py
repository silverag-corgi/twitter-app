import math
from enum import Enum, IntEnum
from logging import Logger
from typing import Any, Optional

import python_lib_for_me as pyl
import tweepy
from tweepy.models import SearchResults

from twitter_app.util import const_util


class EnumOfSearchResultType(Enum):
    MIXED = 'mixed'         # 最新の検索結果と人気のある検索結果
    RECENT = 'recent'       # 最新の検索結果のみ
    POPULAR = 'popular'     # 人気のある検索結果のみ


class EnumOfTweetsInPast7Day():
    class EnumOfOauth1User(IntEnum):
        MAX_NUM_OF_DATA_PER_REQUEST = 100
        MAX_NUM_OF_REQUESTS_PER_15MIN = 180
        MAX_NUM_OF_DATA_PER_15MIN = MAX_NUM_OF_DATA_PER_REQUEST * MAX_NUM_OF_REQUESTS_PER_15MIN
    
    class EnumOfOauth2App(IntEnum):
        MAX_NUM_OF_DATA_PER_REQUEST = 100
        MAX_NUM_OF_REQUESTS_PER_15MIN = 450
        MAX_NUM_OF_DATA_PER_15MIN = MAX_NUM_OF_DATA_PER_REQUEST * MAX_NUM_OF_REQUESTS_PER_15MIN


def search_tweets_in_past_7day(
        api: tweepy.API,
        query: str,
        search_result_type: EnumOfSearchResultType,
        num_of_data: int = EnumOfTweetsInPast7Day.EnumOfOauth1User.MAX_NUM_OF_DATA_PER_15MIN.value,
        num_of_data_per_request: int =
        EnumOfTweetsInPast7Day.EnumOfOauth1User.MAX_NUM_OF_DATA_PER_REQUEST.value
    ) -> list[SearchResults]:
    
    '''
    ツイート検索(過去7日間)
    
    Args:
        api (tweepy.API)                            : API
        query (str)                                 : クエリ
        search_result_type (EnumOfSearchResultType) : 検索結果の種類
        num_of_data (int, optional)                 : データ数
        num_of_data_per_request (int, optional)     : リクエストごとのデータ数
    
    Returns:
        list[SearchResults] : ツイート検索結果ページ (list[SearchResults[tweepy.models.Status]])
    
    Notes:
        - 認証
            - ユーザ認証(OAuth 1.0a)
            - アプリ認証(OAuth 2.0)
        - エンドポイント
            - GET search/tweets
        - レート制限
            - ユーザ認証(OAuth 1.0a)
                - データ数／リクエスト : 100
                - リクエスト数／１５分 : 180
                    - 超過した場合は15分の待機時間が発生する
            - アプリ認証(OAuth 2.0)
                - データ数／リクエスト : 100
                - リクエスト数／１５分 : 450
                    - 超過した場合は15分の待機時間が発生する
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets
        - パラメータ
            - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/guides/standard-operators
        - レスポンス
            - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets#example-response
            - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    tweet_search_result_pages: list[SearchResults] = []
    
    # 認証方式の確認
    if isinstance(api.auth, (tweepy.OAuth1UserHandler, tweepy.OAuth2AppHandler)) == False:
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
        
        # リクエスト数の算出
        num_of_requests = math.ceil(num_of_data / num_of_data_per_request)
        
        # ツイートの検索
        tweet_search_result_pagination: tweepy.Cursor = tweepy.Cursor(
                api.search_tweets,
                q=query,
                result_type=search_result_type.value,
                count=num_of_data_per_request
            )
        tweet_search_result_pages = list(tweet_search_result_pagination.pages(num_of_requests))
        
        pyl.log_inf(lg, f'ツイート検索(過去7日間)に成功しました。(query:{query})')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'ツイート検索(過去7日間)に失敗しました。(query:{query})')
        raise(e)
    
    return tweet_search_result_pages


class CustomStream(tweepy.Stream):
    def __init__(self, auth: Any, following_user_ids: Optional[list[str]], **kwargs: Any) -> None:
        super().__init__(
                auth.consumer_key,
                auth.consumer_secret,
                auth.access_token,
                auth.access_token_secret,
                **kwargs
            )
        self.__following_user_ids = following_user_ids
        self.__tweet_num = 0
    
    def on_status(self, tweet: Any) -> None:
        try:
            lg: Logger = pyl.get_logger(__name__)
            
            # ツイート表示要否の判定(通常ツイート、リツイート、リプライの場合)
            display_tweet: bool = True
            if hasattr(tweet, 'retweeted_status') == True:  # リツイートの場合
                if self.__following_user_ids is None:
                    # フォローユーザIDが存在しない場合
                    display_tweet = False
                elif tweet.user.id not in self.__following_user_ids:
                    # ツイート元ユーザIDがフォローユーザID内に存在しない場合
                    display_tweet = False
            elif tweet.in_reply_to_user_id is not None:     # リプライの場合
                if self.__following_user_ids is None:
                    # フォローユーザIDが存在しない場合
                    display_tweet = False
                elif tweet.in_reply_to_user_id not in self.__following_user_ids \
                    or tweet.user.id not in self.__following_user_ids:
                    # 返信先ユーザIDまたは、返信元ユーザIDがフォローユーザID内に存在しない場合
                    display_tweet = False
            
            # ツイートの表示
            if display_tweet == True:
                self.__tweet_num += 1
                user_name: str = tweet.user.name
                user_id: str = tweet.user.screen_name
                text: str = str(tweet.text).replace('\n', '\n    ')
                creation_timestamp: str = pyl.convert_timestamp_to_jst(str(tweet.created_at))
                url: str = const_util.TWEET_URL.format(tweet.user.screen_name, tweet.id)
                pyl.log_inf(lg, f'ツイート番号：{self.__tweet_num:04}\n' +
                                f'    {user_name} (@{user_id})\n' +
                                f'    {text}\n' +
                                f'    {creation_timestamp}\n' +
                                f'    {url}')
        except Exception as e:
            raise(e)


class EnumOfStream(IntEnum):
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
        following_user_ids (Optional[list[str]])    : フォローユーザID (×：screen_name、〇：user_id)
        keywords (Optional[list[str]])              : キーワード
    
    Returns:
        -
    
    Notes:
        - 認証
            - ユーザ認証(OAuth 1.0a)
        - エンドポイント
            - POST statuses/filter
        - レート制限
            - ユーザ認証(OAuth 1.0a)
                - リクエスト数／１５分 : (未公表)
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/filter-realtime/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/filter-realtime/api-reference/post-statuses-filter
        - パラメータ
            - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/filter-realtime/guides/basic-stream-parameters#follow
            - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/filter-realtime/guides/basic-stream-parameters#track
        - レスポンス
            - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    # 認証方式の確認
    if isinstance(api.auth, (tweepy.OAuth1UserHandler)) == False:
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        
        # ストリームの生成
        stream: CustomStream = CustomStream(
                api.auth,
                following_user_ids
            )
        
        # ツイートの配信
        stream.filter(follow=following_user_ids, track=keywords, languages=['ja'])
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'ツイート配信に失敗しました。')
        raise(e)
    
    return None

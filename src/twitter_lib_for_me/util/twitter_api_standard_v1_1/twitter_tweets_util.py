from enum import Enum, IntEnum
from logging import Logger
from typing import Any, Optional

import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet


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
        num_of_data_per_request: int = int(TWEETS_IN_PAST_7DAY.MAX_NUM_OF_DATA_PER_REQUEST),
        num_of_requests: int = int(TWEETS_IN_PAST_7DAY.MAX_NUM_OF_REQUESTS_PER_15MIN)
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
        list[ResultSet] : ツイート検索結果ページ (list[list[tweepy.models.SearchResults]])
    
    Notes:
        - 引数「リクエストごとのデータ数」は上限が100データ
            - 超過して指定した場合は上限で上書きする
        - 引数「リクエスト数」は15分ごとに最大180リクエスト
            - 超過して指定した場合はレート制限により15分の待機時間が発生する
        - 15分で最大18000データを取得できる
            - 100 data/req * 180 req/15-min = 18000 data/15-min
    
    References:
        - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets
        - https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/guides/standard-operators
        - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        tweet_search_result_pages: list[ResultSet] = []
        
        pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
        try:
            tweet_search_result_pagination: tweepy.Cursor = tweepy.Cursor(
                    api.search_tweets,
                    q=query,
                    result_type=search_result_type,
                    count=num_of_data_per_request
                    if num_of_data_per_request <= int(
                        TWEETS_IN_PAST_7DAY.MAX_NUM_OF_DATA_PER_REQUEST)
                    else int(TWEETS_IN_PAST_7DAY.MAX_NUM_OF_DATA_PER_REQUEST)
                )
            tweet_search_result_pages = list(tweet_search_result_pagination.pages(num_of_requests))
        except Exception as e:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_war(lg, f'検索する際にエラーが発生しました。' +
                            f'(query:{query}, err_msg:{err_msg})')
    except Exception as e:
        raise(e)
    
    return tweet_search_result_pages


def has_twitter_list(api: tweepy.API, twitter_list_name: str) -> bool:
    '''Twitterリスト存在有無確認'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        twitter_lists: Any = api.get_lists()
        
        for twitter_list in twitter_lists:
            if twitter_list.name == twitter_list_name:
                pyl.log_inf(lg, f'Twitterリストが既に存在します。(twitter_list_name:{twitter_list_name})')
                return True
    except Exception as e:
        raise(e)
    
    return False


def generate_twitter_list(api: tweepy.API, twitter_list_name: str) -> tweepy.List:
    '''Twitterリスト生成'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        twitter_list: Any = api.create_list(twitter_list_name, mode='private', description='')
        pyl.log_inf(lg, f'Twitterリスト生成に成功しました。(twitter_list_name:{twitter_list_name})')
    except Exception as e:
        if lg is not None:
            pyl.log_war(lg, f'Twitterリスト生成に失敗しました。(twitter_list_name:{twitter_list_name})')
        raise(e)
    
    return twitter_list


def destroy_twitter_list(api: tweepy.API, twitter_list: tweepy.List) -> None:
    '''Twitterリスト破棄'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        api.destroy_list(list_id=twitter_list.id)
        pyl.log_inf(lg, f'Twitterリスト破棄に成功しました。(twitter_list:{twitter_list.name})')
    except Exception as e:
        if lg is not None:
            pyl.log_war(lg, f'Twitterリスト破棄に失敗しました。(twitter_list:{twitter_list.name})')
        raise(e)
    
    return None


def add_user(api: tweepy.API, twitter_list: tweepy.List, user_id: str, user_name: str) -> bool:
    '''ユーザ追加'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        api.add_list_member(list_id=twitter_list.id, screen_name=user_id)
        pyl.log_deb(lg, f'ユーザ追加に成功しました。(user_id:{user_id: <15}, user_name:{user_name})')
    except Exception as e:
        if lg is not None:
            pyl.log_war(lg, f'ユーザ追加に失敗しました。鍵付きや削除済みの可能性があります。' +
                            f'(user_id:{user_id: <15}, user_name:{user_name})')
        return False
    
    return True

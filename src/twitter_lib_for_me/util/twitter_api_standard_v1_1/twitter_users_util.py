from enum import IntEnum
from logging import Logger
from typing import Any, Optional

import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet


class Followee(IntEnum):
    MAX_NUM_OF_DATA_PER_REQUEST = 200
    MAX_NUM_OF_REQUESTS_PER_15MIN = 15


def get_followee_list_pages(
        api: tweepy.API,
        user_id: str,
        num_of_data_per_request: int = Followee.MAX_NUM_OF_DATA_PER_REQUEST.value,
        num_of_requests: int = Followee.MAX_NUM_OF_REQUESTS_PER_15MIN.value
    ) -> list[ResultSet]:
    
    '''
    フォロイーリストページ取得
    
    Args:
        api (tweepy.API)                : API
        user_id (str)                   : ユーザID
        num_of_data_per_request (int)   : リクエストごとのデータ数(デフォルト：200)
        num_of_requests (int)           : リクエスト数(デフォルト：15)
    
    Returns:
        list[ResultSet] : フォロイーリストページ (list[list[tweepy.models.User]])
    
    Notes:
        - 引数「リクエストごとのデータ数」は上限が200データ
            - 超過して指定した場合は200で上書きする
        - 引数「リクエスト数」は15分ごとに最大15リクエスト
            - 超過して指定した場合はレート制限により15分の待機時間が発生する
        - 15分で最大3000データを取得できる
            - 200 data/req * 15 req/15-min = 3000 data/15-min
    
    References:
        - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-friends-list
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    followee_list_pages: list[ResultSet] = []
    
    try:
        lg = pyl.get_logger(__name__)
        
        pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
        
        followee_pagination: tweepy.Cursor = tweepy.Cursor(
                api.get_friends,
                screen_name=user_id,
                count=num_of_data_per_request
                if num_of_data_per_request <= Followee.MAX_NUM_OF_DATA_PER_REQUEST.value
                else Followee.MAX_NUM_OF_DATA_PER_REQUEST.value
            )
        followee_list_pages = list(followee_pagination.pages(num_of_requests))
    except Exception as e:
        if lg is not None:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_war(lg, f'指定したユーザIDのフォロイーを取得する際にエラーが発生しました。' +
                            f'(user_id:{user_id}, err_msg:{err_msg})')
    
    return followee_list_pages


class Follower(IntEnum):
    MAX_NUM_OF_DATA_PER_REQUEST = 200
    MAX_NUM_OF_REQUESTS_PER_15MIN = 15


def get_follower_list_pages(
        api: tweepy.API,
        user_id: str,
        num_of_data_per_request: int = Follower.MAX_NUM_OF_DATA_PER_REQUEST.value,
        num_of_requests: int = Follower.MAX_NUM_OF_REQUESTS_PER_15MIN.value
    ) -> list[ResultSet]:
    
    '''
    フォロワーリストページ取得
    
    Args:
        api (tweepy.API)                : API
        user_id (str)                   : ユーザID
        num_of_data_per_request (int)   : リクエストごとのデータ数(デフォルト：200)
        num_of_requests (int)           : リクエスト数(デフォルト：15)
    
    Returns:
        list[ResultSet] : フォロワーリストページ (list[list[tweepy.models.User]])
    
    Notes:
        - 「フォロイーリストページ取得」を参照する
    
    References:
        - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-followers-list
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    follower_list_pages: list[ResultSet] = []
    
    try:
        lg = pyl.get_logger(__name__)
        
        pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
        
        follower_pagination: tweepy.Cursor = tweepy.Cursor(
                api.get_followers,
                screen_name=user_id,
                count=num_of_data_per_request
                if num_of_data_per_request <= Follower.MAX_NUM_OF_DATA_PER_REQUEST.value
                else Follower.MAX_NUM_OF_DATA_PER_REQUEST.value
            )
        follower_list_pages = list(follower_pagination.pages(num_of_requests))
    except Exception as e:
        if lg is not None:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_war(lg, f'指定したユーザIDのフォロワーを取得する際にエラーが発生しました。' +
                            f'(user_id:{user_id}, err_msg:{err_msg})')
    
    return follower_list_pages


def get_user_info(
        api: tweepy.API,
        user_id: str
    ) -> Any:
    
    '''
    ユーザ情報取得
    
    Args:
        api (tweepy.API)    : API
        user_id (str)       : ユーザID
    
    Returns:
        Any: ユーザ情報 (tweepy.models.User)
    
    References:
        - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-users-show
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        user_info: Any = api.get_user(screen_name=user_id)
        
        pyl.log_deb(lg, f'ユーザ情報取得に成功しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'ユーザ情報取得に失敗しました。')
        raise(e)
    
    return user_info


def has_twitter_list(api: tweepy.API, twitter_list_name: str) -> bool:
    '''Twitterリスト存在有無確認'''
    
    lg: Optional[Logger] = None
    result: bool = False
    
    try:
        lg = pyl.get_logger(__name__)
        
        twitter_lists: Any = api.get_lists()
        
        for twitter_list in twitter_lists:
            if twitter_list.name == twitter_list_name:
                pyl.log_inf(lg, f'Twitterリストが既に存在します。(twitter_list_name:{twitter_list_name})')
                result = True
                break
    except Exception as e:
        if lg is not None:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_war(lg, f'Twitterリスト存在有無確認に失敗しました。' +
                            f'(twitter_list_name:{twitter_list_name}, err_msg:{err_msg})')
    
    return result


def generate_twitter_list(api: tweepy.API, twitter_list_name: str) -> tweepy.List:
    '''Twitterリスト生成'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        twitter_list: Any = api.create_list(twitter_list_name, mode='private', description='')
        pyl.log_inf(lg, f'Twitterリスト生成に成功しました。(twitter_list_name:{twitter_list_name})')
    except Exception as e:
        if lg is not None:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_war(lg, f'Twitterリスト生成に失敗しました。' +
                            f'(twitter_list_name:{twitter_list_name}, err_msg:{err_msg})')
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
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_war(lg, f'Twitterリスト破棄に失敗しました。' +
                            f'(twitter_list:{twitter_list.name}, err_msg:{err_msg})')
        raise(e)
    
    return None


def add_user(api: tweepy.API, twitter_list: tweepy.List, user_id: str, user_name: str) -> bool:
    '''ユーザ追加'''
    
    lg: Optional[Logger] = None
    result: bool = False
    
    try:
        lg = pyl.get_logger(__name__)
        
        api.add_list_member(list_id=twitter_list.id, screen_name=user_id)
        pyl.log_deb(lg, f'ユーザ追加に成功しました。(user_id:{user_id: <15}, user_name:{user_name})')
        
        result = True
    except Exception as e:
        if lg is not None:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_war(lg, f'ユーザ追加に失敗しました。鍵付きや削除済みの可能性があります。' +
                            f'(user_id:{user_id: <15}, user_name:{user_name}, err_msg:{err_msg})')
    
    return result

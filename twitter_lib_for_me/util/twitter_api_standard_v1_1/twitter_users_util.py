from enum import IntEnum
from logging import Logger
from typing import Optional

import python_lib_for_me as mylib
import tweepy
from tweepy.models import ResultSet


class Followee(IntEnum):
    MAX_NUM_OF_DATA_PER_REQUEST = 200
    MAX_NUM_OF_REQUESTS_PER_15MIN = 15


def get_followee_list_pages(
        api: tweepy.API,
        user_id: str,
        num_of_data_per_request: int = Followee.MAX_NUM_OF_DATA_PER_REQUEST,
        num_of_requests: int = Followee.MAX_NUM_OF_REQUESTS_PER_15MIN
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
    '''
    
    lg: Optional[Logger] = None
    
    try:
        lg = mylib.get_logger(__name__)
        
        followee_list_pages: list[ResultSet] = []
        
        lg.info(f'時間がかかるため気長にお待ちください。')
        try:
            followee_pagination: tweepy.Cursor = tweepy.Cursor(
                    api.get_friends,
                    screen_name=user_id,
                    count=num_of_data_per_request \
                        if num_of_data_per_request <= Followee.MAX_NUM_OF_DATA_PER_REQUEST
                        else Followee.MAX_NUM_OF_DATA_PER_REQUEST
                )
            followee_list_pages = list(followee_pagination.pages(num_of_requests))
        except Exception as e:
            err_msg: str = str(e).replace('\n',' ')
            lg.warning(f'指定したユーザIDのフォロイーを取得する際にエラーが発生しました。' +
                        f'(user_id:{user_id}, err_msg:{err_msg})')
    except Exception as e:
        raise(e)
    
    return followee_list_pages


class Follower(IntEnum):
    MAX_NUM_OF_DATA_PER_REQUEST = 200
    MAX_NUM_OF_REQUESTS_PER_15MIN = 15


def get_follower_list_pages(
        api: tweepy.API,
        user_id: str,
        num_of_data_per_request: int = Follower.MAX_NUM_OF_DATA_PER_REQUEST,
        num_of_requests: int = Follower.MAX_NUM_OF_REQUESTS_PER_15MIN
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
    '''
    
    lg: Optional[Logger] = None
    
    try:
        lg = mylib.get_logger(__name__)
        
        follower_list_pages: list[ResultSet] = []
        
        lg.info(f'時間がかかるため気長にお待ちください。')
        try:
            follower_pagination: tweepy.Cursor = tweepy.Cursor(
                    api.get_followers,
                    screen_name=user_id,
                    count=num_of_data_per_request \
                        if num_of_data_per_request <= Follower.MAX_NUM_OF_DATA_PER_REQUEST
                        else Follower.MAX_NUM_OF_DATA_PER_REQUEST
                )
            follower_list_pages = list(follower_pagination.pages(num_of_requests))
        except Exception as e:
            err_msg: str = str(e).replace('\n',' ')
            lg.warning(f'指定したユーザIDのフォロワーを取得する際にエラーが発生しました。' +
                        f'(user_id:{user_id}, err_msg:{err_msg})')
    except Exception as e:
        raise(e)
    
    return follower_list_pages

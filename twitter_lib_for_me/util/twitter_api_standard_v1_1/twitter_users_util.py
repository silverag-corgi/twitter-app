from logging import Logger
from typing import Optional

import python_lib_for_me as mylib
import tweepy
from tweepy.models import ResultSet


def get_followee_pages(
        api: tweepy.API,
        user_id: str,
        max_num_of_data_per_request: int = 200,
        max_num_of_requests: int = 15
    ) -> list[ResultSet]:
    
    '''
    フォロイーページ取得
    
    Args:
        api (tweepy.API)                    : API
        user_id (str)                       : ユーザID
        max_num_of_data_per_request (int)   : リクエストごとの最大データ数(デフォルト：200)
        max_num_of_requests (int)           : 最大リクエスト数(デフォルト：15)
    
    Returns:
        list[ResultSet] : フォロイーページ (list[list[tweepy.models.User]])
    
    Notes:
        - 引数「リクエストごとの最大データ数」の上限は200データ
            - 超過して指定した場合は200で上書きする
        - 引数「最大リクエスト数」は15分ごとに最大15リクエスト
            - 超過して指定した場合はレート制限により15分の待機時間が発生する
        - 15分で最大3000データを取得できる
            - 200 data/req * 15 req/15-min = 3000 data/15-min
    
    References:
        - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-friends-list
    '''
    
    lg: Optional[Logger] = None
    
    try:
        lg = mylib.get_logger(__name__)
        
        followee_pages: list[ResultSet] = []
        
        lg.info(f'時間がかかるため気長にお待ちください。')
        try:
            followee_pagination: tweepy.Cursor = tweepy.Cursor(
                    api.get_friends,
                    screen_name=user_id,
                    count=max_num_of_data_per_request if max_num_of_data_per_request <= 200 else 200
                )
            followee_pages = list(followee_pagination.pages(max_num_of_requests))
        except Exception as e:
            err_msg: str = str(e).replace('\n',' ')
            lg.warning(f'指定したユーザIDのフォロイーを取得する際にエラーが発生しました。' +
                        f'(user_id:{user_id}, err_msg:{err_msg})')
    except Exception as e:
        raise(e)
    
    return followee_pages

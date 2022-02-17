from logging import Logger
from typing import Optional

import python_lib_for_me as mylib
import tweepy
from tweepy.models import ResultSet


def get_followee_pages(
        api: tweepy.API,
        user_id: str,
        max_num_of_data_per_request: int = 200,
        num_of_requests_per_15min: int = 15
    ) -> list[ResultSet]:
    
    '''
    フォロイーページ取得
    
    Args:
        api (tweepy.API)                    : API
        user_id (str)                       : ユーザID
        max_num_of_data_per_request (int)   : リクエストごとのデータ最大数(デフォルト(上限)：200)
        num_of_requests_per_15min (int)     : 15分ごとのリクエスト数(デフォルト(最適)：15)
    
    Returns:
        list[ResultSet] : フォロイーページ (list[list[tweepy.models.User]])
    
    Memo:
        - 15分で3000件までがレート制限なし
            - 200 data/req * 15 req/15-min = 3000 data/15-min
        - その件数を超過するとレート制限により待機発生
    
    References:
        - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-friends-list
    '''
    
    lg: Optional[Logger] = None
    
    try:
        lg = mylib.get_logger(__name__)
        
        followee_pages: list[ResultSet] = []
        
        if max_num_of_data_per_request > 200:
            max_num_of_data_per_request = 200
        
        lg.info(f'時間がかかるため気長にお待ちください。')
        try:
            followee_pagination: tweepy.Cursor = tweepy.Cursor(
                    api.get_friends,
                    screen_name=user_id,
                    count=max_num_of_data_per_request
                )
            followee_pages = list(followee_pagination.pages(num_of_requests_per_15min))
        except Exception as e:
            err_msg: str = str(e).replace('\n',' ')
            lg.warning(f'指定したユーザIDのフォロイーを取得する際にエラーが発生しました。' +
                        f'(user_id:{user_id}, err_msg:{err_msg})')
    except Exception as e:
        raise(e)
    
    return followee_pages

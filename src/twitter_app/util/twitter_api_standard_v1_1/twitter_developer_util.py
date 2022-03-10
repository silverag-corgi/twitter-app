import json
from datetime import datetime
from logging import Logger
from typing import Any, Optional

import python_lib_for_me as pyl
import tweepy


def show_rate_limit(
        api: tweepy.API,
        resource_family: str,
        endpoint: str
    ) -> None:
    
    '''
    レート制限表示
    
    Args:
        api (tweepy.API)        : API
        resource_family (str)   : リソース群
        endpoint (str)          : エンドポイント
    
    Returns:
        -
    
    Notes:
        - 使用するエンドポイントはGETメソッドである
        - Twitter API Standard v1.1 に対してのみ正確である
        - レート制限を表示できるエンドポイントはGETメソッドのみである
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/developer-utilities/rate-limit-status/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/developer-utilities/rate-limit-status/api-reference/get-application-rate_limit_status
        - レート制限(Standard v1.1)
            - https://developer.twitter.com/en/docs/twitter-api/v1/rate-limits
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        rate_limits: Any = api.rate_limit_status()
        if resource_family != '' and endpoint != '':
            rate_limit: dict = rate_limits['resources'][resource_family][endpoint]
            remaining: int = rate_limit['remaining']
            limit: int = rate_limit['limit']
            reset_datetime: datetime = datetime.fromtimestamp(rate_limit['reset'])
            pyl.log_inf(lg, f'リクエスト回数(15分間隔)：{remaining}/{limit}、' +
                            f'制限リセット時刻：{reset_datetime}')
        else:
            pyl.log_inf(lg, f'レート制限：\n{json.dumps(rate_limits, indent=2)}')
    except Exception as e:
        if lg is not None:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_war(lg, f'レート制限を取得する際にエラーが発生しました。' +
                            f'(resource_family:{resource_family}, ' +
                            f'endpoint:{endpoint}, ' +
                            f'err_msg:{err_msg})')
    
    return None


def show_rate_limit_of_friends_list(api: tweepy.API) -> None:
    '''レート制限表示(GET friends/list)'''
    show_rate_limit(api, 'friends', '/friends/list')
    return None


def show_rate_limit_of_followers_list(api: tweepy.API) -> None:
    '''レート制限表示(GET followers/list)'''
    show_rate_limit(api, 'followers', '/followers/list')
    return None


def show_rate_limit_of_search_tweets(api: tweepy.API) -> None:
    '''レート制限表示(GET search/tweets)'''
    show_rate_limit(api, 'search', '/search/tweets')
    return None

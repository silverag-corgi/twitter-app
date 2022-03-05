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
    
    '''レート制限表示'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        rate_limits: Any = api.rate_limit_status()
        if resource_family != '' and endpoint != '':
            rate_limit: dict = rate_limits['resources'][resource_family][endpoint]
            pyl.log_inf(lg, f'リクエスト回数(15分間隔)：{rate_limit["remaining"]}/{rate_limit["limit"]}、' +
                            f'制限リセット時刻：{datetime.fromtimestamp(rate_limit["reset"])}')
        else:
            pyl.log_inf(lg, f'レート制限：\n{json.dumps(rate_limits, indent=4)}')
    except Exception as e:
        if lg is not None:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_war(lg, f'レート制限を取得する際にエラーが発生しました。' +
                            f'(resource_family:{resource_family}, ' +
                            f'endpoint:{endpoint}, ' +
                            f'err_msg:{err_msg})')
    
    return None


def show_rate_limit_of_friends_list(api: tweepy.API) -> None:
    '''レート制限表示(friends/list)'''
    show_rate_limit(api, 'friends', '/friends/list')
    return None


def show_rate_limit_of_followers_list(api: tweepy.API) -> None:
    '''レート制限表示(followers/list)'''
    show_rate_limit(api, 'followers', '/followers/list')
    return None


def show_rate_limit_of_search_tweets(api: tweepy.API) -> None:
    '''レート制限表示(search/tweets)'''
    show_rate_limit(api, 'search', '/search/tweets')
    return None

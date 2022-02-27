'''
TwitterAPI共通パッケージ
(Twitter API - Standard v1.1)
https://developer.twitter.com/en/docs/api-reference-index#twitter-api-standard
'''

import math
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl

from .twitter_developer_util import *
from .twitter_dm_util import *
from .twitter_geo_util import *
from .twitter_media_util import *
from .twitter_trends_util import *
from .twitter_tweets_util import *
from .twitter_users_util import *


def show_estimated_proc_time(
        max_num_of_data_per_request: int,
        max_num_of_requests_per_15min: int,
        num_of_data: int
    ) -> None:
    
    '''想定処理時間表示'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        max_num_of_data_per_15min: int = max_num_of_data_per_request * max_num_of_requests_per_15min
        num_of_procs: int = math.ceil(num_of_data / max_num_of_data_per_15min)
        proc_time: int = num_of_procs * 15
        
        pyl.log_inf(lg, f'想定処理時間：約{proc_time}分(TwitterAPIのレート制限により処理に時間がかかります)')
    except Exception as e:
        raise(e)
    
    return None

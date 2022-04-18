import math
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl

from .const_util import *
from .pandas_util import *
from .twitter_api_v1_1 import *


def show_estimated_proc_time(
        num_of_data: int,
        max_num_of_data_per_windows_minutes: int,
        windows_minutes: int = 15
    ) -> None:
    
    '''想定処理時間表示'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        proc_time: int = \
            math.ceil(num_of_data / max_num_of_data_per_windows_minutes) * windows_minutes
        
        pyl.log_inf(lg, f'想定処理時間：約{proc_time}分(TwitterAPIのレート制限により処理に時間がかかります)')
    except Exception as e:
        raise(e)
    
    return None

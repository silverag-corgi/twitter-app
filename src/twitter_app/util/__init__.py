import math
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl

from .const_util import *
from .pandas_util import *
from .twitter_api_v1_1 import *


def show_estimated_proc_time(
    use_debug_mode: bool,
    num_of_data: int,
    num_of_data_per_minute_interval: int,
    minute_interval: int = 15,
) -> None:
    """想定処理時間表示"""

    clg: Optional[pyl.CustomLogger] = None

    try:
        clg = pyl.CustomLogger(__name__, use_debug_mode=use_debug_mode)

        proc_time: int = math.ceil(num_of_data / num_of_data_per_minute_interval) * minute_interval

        clg.log_inf(f"想定処理時間：約{proc_time}分(TwitterAPIのレート制限により処理に時間がかかります)")
    except Exception as e:
        raise (e)

    return None

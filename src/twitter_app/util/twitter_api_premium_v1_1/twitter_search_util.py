from enum import Enum, IntEnum, auto
from logging import Logger
from typing import Callable, Optional

import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet


class SEARCH_API(IntEnum):
    WITHIN_LAST_30DAY = auto()  # 検索API(過去30日以内)
    FULL_ARCHIVE = auto()       # 検索API(フルアーカイブ)


class ENV_LABEL(Enum):
    WITHIN_LAST_30DAY = 'dev'   # 環境ラベル(過去30日以内)
    FULL_ARCHIVE = 'dev'        # 環境ラベル(フルアーカイブ)


class TWEETS(IntEnum):
    MAX_NUM_OF_DATA_PER_REQUEST = 100
    MAX_NUM_OF_REQUESTS_PER_MIN = 30


def search_tweets(
        api: tweepy.API,
        query: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        search_api: SEARCH_API = SEARCH_API.WITHIN_LAST_30DAY,
        env_label: ENV_LABEL = ENV_LABEL.WITHIN_LAST_30DAY,
        num_of_data_per_request: int = TWEETS.MAX_NUM_OF_DATA_PER_REQUEST.value,
        num_of_requests: int = TWEETS.MAX_NUM_OF_REQUESTS_PER_MIN.value
    ) -> list[ResultSet]:
    
    '''
    ツイート検索(過去30日以内／フルアーカイブ)
    
    Args:
        api (tweepy.API)                        : API
        query (str)                             : クエリ
        start_date (Optional[str], optional)    : 検索開始日付(JST)(yyyy-mm-dd hh:mm形式)
        end_date (Optional[str], optional)      : 検索終了日付(JST)(yyyy-mm-dd hh:mm形式)
        search_api (SEARCH_API, optional)       : 検索API(デフォルト：過去30日以内)
        env_label (ENV_LABEL, optional)         : 環境ラベル(デフォルト：過去30日以内)
        num_of_data_per_request (int, optional) : リクエストごとのデータ数(デフォルト：100)
        num_of_requests (int, optional)         : リクエスト数(デフォルト：30)
    
    Returns:
        list[ResultSet] : ツイートページ (list[ResultSet[tweepy.models.Status]])
    
    Notes:
        - 使用するエンドポイントはPOSTメソッドである
        - 検索日付の大小関係は以下の通りである
            - 検索開始日付 <= 検索期間 < 検索終了日付
        - 引数「リクエストごとのデータ数」は上限が100データ
            - 超過して指定した場合は上限で上書きする
        - 引数「リクエスト数」は1分ごとに最大30リクエスト
            - 超過して指定した場合はレート制限により1分の待機時間が発生する
            - 1秒ごとに最大10リクエスト、1ヶ月に250リクエスト、1ヶ月に2.5万ツイート
        - 1分で最大3000データを取得できる
            - 100 data/req * 30 req/min = 3000 data/min
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/premium/search-api/overview
            - https://developer.twitter.com/en/docs/twitter-api/premium/search-api/api-reference/premium-search
            - https://developer.twitter.com/en/docs/twitter-api/premium/rules-and-filtering/operators-by-product
        - オブジェクトモデル
            - https://developer.twitter.com/en/docs/twitter-api/premium/data-dictionary/object-model/tweet
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        # 検索開始日付、検索終了日付のUTC変換
        start_date_utc: Optional[str] = None
        if start_date is not None:
            start_date_utc = pyl.convert_timestamp_to_utc(
                    start_date,
                    src_timestamp_format='%Y-%m-%d %H:%M',
                    utc_timestamp_format='%Y%m%d%H%M'
                )
        end_date_utc: Optional[str] = None
        if end_date is not None:
            end_date_utc = pyl.convert_timestamp_to_utc(
                    end_date,
                    src_timestamp_format='%Y-%m-%d %H:%M',
                    utc_timestamp_format='%Y%m%d%H%M'
                )
        
        # 検索APIの決定
        search_api_function: Callable
        if search_api == SEARCH_API.WITHIN_LAST_30DAY:
            search_api_function = api.search_30_day
        elif search_api == SEARCH_API.FULL_ARCHIVE:
            search_api_function = api.search_full_archive
        
        # ツイートの検索
        tweet_search_result_pages: list[ResultSet] = []
        try:
            pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
            
            tweet_search_result_pagination: tweepy.Cursor = tweepy.Cursor(
                    search_api_function,
                    label=env_label.value,
                    query=query,
                    fromDate=start_date_utc,
                    toDate=end_date_utc,
                    maxResults=num_of_data_per_request
                    if (num_of_data_per_request <=
                        TWEETS.MAX_NUM_OF_DATA_PER_REQUEST.value)
                    else TWEETS.MAX_NUM_OF_DATA_PER_REQUEST.value
                )
            tweet_search_result_pages = list(tweet_search_result_pagination.pages(num_of_requests))
            
            pyl.log_inf(lg, f'ツイート検索(過去30日以内／フルアーカイブ)に成功しました。')
        except Exception as e:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_war(lg, f'ツイート検索(過去30日以内／フルアーカイブ)に失敗しました。' +
                            f'(query:{query}, err_msg:{err_msg})')
    except Exception as e:
        raise(e)
    
    return tweet_search_result_pages

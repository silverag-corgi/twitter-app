from enum import IntEnum
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet


class TWEETS_WITHIN_LAST_30DAY(IntEnum):
    MAX_NUM_OF_DATA_PER_REQUEST = 100
    MAX_NUM_OF_REQUESTS_PER_MIN = 30


def search_tweets_within_last_30day(
        api: tweepy.API,
        query: str,
        start_date: str,
        end_date: str,
        num_of_data_per_request: int = int(TWEETS_WITHIN_LAST_30DAY.MAX_NUM_OF_DATA_PER_REQUEST),
        num_of_requests: int = int(TWEETS_WITHIN_LAST_30DAY.MAX_NUM_OF_REQUESTS_PER_MIN)
    ) -> list[ResultSet]:
    
    '''
    ツイート検索(過去30日以内)
    
    Args:
        api (tweepy.API)                        : API
        query (str)                             : クエリ
        start_date (str)                        : 検索開始日付(yyyymmddhhmm形式)
        end_date (str)                          : 検索終了日付(yyyymmddhhmm形式)
        num_of_data_per_request (int, optional) : リクエストごとのデータ数(デフォルト：100)
        num_of_requests (int, optional)         : リクエスト数(デフォルト：30)
    
    Returns:
        list[ResultSet] : ツイートページ (list[list[tweepy.models.Status]])
    
    Notes:
        - 引数「リクエストごとのデータ数」は上限が100データ
            - 超過して指定した場合は上限で上書きする
        - 引数「リクエスト数」は1分ごとに最大30リクエスト
            - 超過して指定した場合はレート制限により1分の待機時間が発生する
            - 1秒ごとに最大10リクエスト、1ヶ月に250リクエスト、1ヶ月に2.5万ツイート
        - 1分で最大3000データを取得できる
            - 100 data/req * 30 req/min = 3000 data/min
    
    References:
        - https://developer.twitter.com/en/docs/twitter-api/premium/search-api/api-reference/premium-search
        - https://developer.twitter.com/en/docs/twitter-api/premium/rules-and-filtering/operators-by-product
        - https://developer.twitter.com/en/docs/twitter-api/premium/data-dictionary/object-model/tweet
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        tweet_pages: list[ResultSet] = []
        
        if len(query) > 256:
            pyl.log_inf(lg, f'クエリが256文字以下ではありません。(query:{query})')
        else:
            pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
            try:
                tweet_pagination: tweepy.Cursor = tweepy.Cursor(
                        api.search_30_day,
                        label='dev',
                        query=query,
                        fromDate=start_date,
                        toDate=end_date,
                        maxResults=num_of_data_per_request
                        if num_of_data_per_request <= int(
                            TWEETS_WITHIN_LAST_30DAY.MAX_NUM_OF_DATA_PER_REQUEST)
                        else int(TWEETS_WITHIN_LAST_30DAY.MAX_NUM_OF_DATA_PER_REQUEST)
                    )
                tweet_pages = list(tweet_pagination.pages(num_of_requests))
            except Exception as e:
                err_msg: str = str(e).replace('\n', ' ')
                pyl.log_war(lg, f'検索する際にエラーが発生しました。' +
                                f'(query:{query}, err_msg:{err_msg})')
    except Exception as e:
        raise(e)
    
    return tweet_pages

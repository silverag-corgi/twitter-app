import math
from enum import Enum, IntEnum, auto
from typing import Callable, Optional

import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet


class EnumOfSearchApi(IntEnum):
    WITHIN_LAST_30DAY = auto()  # 検索API(過去30日以内)
    FULL_ARCHIVE = auto()  # 検索API(フルアーカイブ)


class EnumOfEnvLabel(Enum):
    WITHIN_LAST_30DAY = "dev"  # 環境ラベル(過去30日以内)
    FULL_ARCHIVE = "dev"  # 環境ラベル(フルアーカイブ)


class EnumOfTweets:
    class EnumOfOauth2App(IntEnum):
        MAX_NUM_OF_DATA_PER_REQUEST = 100
        MAX_NUM_OF_REQUESTS_PER_MIN = 30
        MAX_NUM_OF_DATA_PER_MIN = MAX_NUM_OF_DATA_PER_REQUEST * MAX_NUM_OF_REQUESTS_PER_MIN


def search_tweets(
    api: tweepy.API,
    query: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    search_api: EnumOfSearchApi = EnumOfSearchApi.WITHIN_LAST_30DAY,
    env_label: EnumOfEnvLabel = EnumOfEnvLabel.WITHIN_LAST_30DAY,
    num_of_data: int = EnumOfTweets.EnumOfOauth2App.MAX_NUM_OF_DATA_PER_MIN.value,
    num_of_data_per_request: int = EnumOfTweets.EnumOfOauth2App.MAX_NUM_OF_DATA_PER_REQUEST.value,
) -> list[ResultSet]:
    """
    ツイート検索(過去30日以内／フルアーカイブ)

    Args:
        api (tweepy.API)                        : API
        query (str)                             : クエリ
        start_date (Optional[str], optional)    : 検索開始日付(JST)(yyyy-mm-dd hh:mm形式)
        end_date (Optional[str], optional)      : 検索終了日付(JST)(yyyy-mm-dd hh:mm形式)
        search_api (EnumOfSearchApi, optional)  : 検索API(デフォルト：過去30日以内)
        env_label (EnumOfEnvLabel, optional)    : 環境ラベル(デフォルト：過去30日以内)
        num_of_data (int, optional)             : データ数
        num_of_data_per_request (int, optional) : リクエストごとのデータ数

    Returns:
        list[ResultSet] : ツイートページ (list[ResultSet[tweepy.models.Status]])

    Notes:
        - 認証
            - アプリ認証(OAuth 2.0)
        - エンドポイント
            - POST /search/:product/:label
        - レート制限
            - アプリ認証(OAuth 2.0)
                - データ数／リクエスト : 100
                - リクエスト数／秒 : 10
                - リクエスト数／分 : 30
                - リクエスト数／月 : 250
                    - 超過した場合は1分の待機時間が発生する
        - 検索開始日付 <= 検索期間 < 検索終了日付

    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/premium/search-api/overview
            - https://developer.twitter.com/en/docs/twitter-api/premium/search-api/api-reference/premium-search
        - パラメータ
            - https://developer.twitter.com/en/docs/twitter-api/premium/rules-and-filtering/operators-by-product
                - 使用したい演算子(is:retweet,is:reply)が有料版でないと使用できない
        - レスポンス
            - https://developer.twitter.com/en/docs/twitter-api/premium/data-dictionary/object-model/tweet
    """  # noqa: E501

    clg: Optional[pyl.CustomLogger] = None
    tweet_search_result_pages: list[ResultSet] = []

    # 認証方式の確認
    if isinstance(api.auth, (tweepy.OAuth2AppHandler)) is False:
        raise (pyl.CustomError(f"この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})"))

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__)

        # 検索開始日付、検索終了日付のUTC変換
        start_date_utc: Optional[str] = None
        if start_date is not None:
            start_date_utc = pyl.convert_timestamp_to_utc(
                start_date,
                src_timestamp_format="%Y-%m-%d %H:%M",
                utc_timestamp_format="%Y%m%d%H%M",
            )
        end_date_utc: Optional[str] = None
        if end_date is not None:
            end_date_utc = pyl.convert_timestamp_to_utc(
                end_date,
                src_timestamp_format="%Y-%m-%d %H:%M",
                utc_timestamp_format="%Y%m%d%H%M",
            )

        # 検索APIの決定
        search_api_function: Callable
        if search_api == EnumOfSearchApi.WITHIN_LAST_30DAY:
            search_api_function = api.search_30_day
        elif search_api == EnumOfSearchApi.FULL_ARCHIVE:
            search_api_function = api.search_full_archive

        # リクエスト数の算出
        num_of_requests = math.ceil(num_of_data / num_of_data_per_request)

        # ツイートの検索
        tweet_search_result_pagination: tweepy.Cursor = tweepy.Cursor(
            search_api_function,
            label=env_label.value,
            query=query,
            fromDate=start_date_utc,
            toDate=end_date_utc,
            maxResults=num_of_data_per_request,
        )
        tweet_search_result_pages = list(tweet_search_result_pagination.pages(num_of_requests))

        clg.log_inf(f"ツイート検索(過去30日以内／フルアーカイブ)に成功しました。(query:{query})")
    except Exception as e:
        if clg is not None:
            clg.log_err(f"ツイート検索(過去30日以内／フルアーカイブ)に失敗しました。(query:{query})")
        raise (e)

    return tweet_search_result_pages

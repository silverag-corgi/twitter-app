import json
from datetime import datetime
from typing import Any, Optional

import python_lib_for_me as pyl
import tweepy


def show_rate_limit(
    use_debug_mode: bool,
    api: tweepy.API,
    resource_family: str,
    endpoint: str,
) -> None:
    """
    レート制限表示

    Args:
        use_debug_mode (bool)   : デバッグモード使用有無
        api (tweepy.API)        : API
        resource_family (str)   : リソース群
        endpoint (str)          : エンドポイント

    Returns:
        -

    Notes:
        - 認証
            - ユーザ認証(OAuth 1.0a)
            - アプリ認証(OAuth 2.0)
        - エンドポイント
            - GET application/rate_limit_status
        - レート制限
            - ユーザ認証(OAuth 1.0a)
                - リクエスト数／１５分 : 180
                    - 超過した場合は15分の待機時間が発生する
            - アプリ認証(OAuth 2.0)
                - リクエスト数／１５分 : 180
                    - 超過した場合は15分の待機時間が発生する
        - Twitter API Standard v1.1 のGETメソッドに対してのみ正確である

    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/developer-utilities/rate-limit-status/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/developer-utilities/rate-limit-status/api-reference/get-application-rate_limit_status
        - レート制限(Standard v1.1)
            - https://developer.twitter.com/en/docs/twitter-api/v1/rate-limits
    """  # noqa: E501

    clg: Optional[pyl.CustomLogger] = None

    # 認証方式の確認
    if isinstance(api.auth, (tweepy.OAuth1UserHandler, tweepy.OAuth2AppHandler)) is False:
        raise (pyl.CustomError(f"この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})"))

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=use_debug_mode)

        # レート制限の表示
        rate_limits: Any = api.rate_limit_status()
        if not (resource_family == "" or endpoint == ""):
            rate_limit: dict = rate_limits["resources"][resource_family][endpoint]
            remaining: int = rate_limit["remaining"]
            limit: int = rate_limit["limit"]
            reset_datetime: datetime = datetime.fromtimestamp(rate_limit["reset"])
            clg.log_inf(
                f"リクエスト回数(15分間隔)：{remaining}/{limit}、制限リセット時刻：{reset_datetime} "
                + f"(resource_family:{resource_family}, endpoint:{endpoint})"
            )
        else:
            clg.log_inf(f"レート制限：\n{json.dumps(rate_limits, indent=2)}")
    except Exception as e:
        if clg is not None:
            clg.log_err(f"レート制限表示に失敗しました。(resource_family:{resource_family}, endpoint:{endpoint})")
        raise (e)

    return None


def show_rate_limit_of_lists_members(
    use_debug_mode: bool,
    api: tweepy.API,
) -> None:
    """レート制限表示(GET lists/members)"""
    show_rate_limit(use_debug_mode, api, "lists", "/lists/members")
    return None


def show_rate_limit_of_friends_list(
    use_debug_mode: bool,
    api: tweepy.API,
) -> None:
    """レート制限表示(GET friends/list)"""
    show_rate_limit(use_debug_mode, api, "friends", "/friends/list")
    return None


def show_rate_limit_of_followers_list(
    use_debug_mode: bool,
    api: tweepy.API,
) -> None:
    """レート制限表示(GET followers/list)"""
    show_rate_limit(use_debug_mode, api, "followers", "/followers/list")
    return None


def show_rate_limit_of_search_tweets(
    use_debug_mode: bool,
    api: tweepy.API,
) -> None:
    """レート制限表示(GET search/tweets)"""
    show_rate_limit(use_debug_mode, api, "search", "/search/tweets")
    return None

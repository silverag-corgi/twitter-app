import argparse
import os
import sys
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth
from twitter_app.main import argument
from twitter_app.util.twitter_api_v1_1.standard import twitter_developer_util


def show_rate_limit(arg_namespace: argparse.Namespace) -> None:
    """
    Twitterレート制限表示

    Summary:
        引数を検証して問題ない場合、指定したリソース群とエンドポイントのレート制限を表示する。

    Args:
        arg_namespace (argparse.Namespace): 引数名前空間

    Returns:
        None
    """

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__)

        # 引数の検証
        arg: argument.TwitterRateLimitShowArg = argument.TwitterRateLimitShowArg(arg_namespace)
        __validate_arg(arg)

        # ロジック(TwitterAPI認証)の実行
        api: tweepy.API = twitter_api_auth.do_logic_that_generate_api_by_oauth_1_user()

        # レート制限の表示
        twitter_developer_util.show_rate_limit(
            api,
            arg.resource_family,
            arg.endpoint,
        )
    except Exception as e:
        raise (e)

    return None


def __validate_arg(arg: argument.TwitterRateLimitShowArg) -> None:
    """引数検証"""

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__)

        # 引数指定の確認
        if arg.is_specified() is False:
            raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

        # 検証：なし
    except Exception as e:
        raise (e)

    return None

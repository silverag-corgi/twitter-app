import argparse
import os
import sys
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth, twitter_followxx_export
from twitter_app.main import argument


def export_twitter_followxx(arg_namespace: argparse.Namespace) -> None:
    """
    Twitterフォロイー(フォロワー)エクスポート

    Summary:
        引数を検証して問題ない場合、指定したユーザのフォロイー(フォロワー)をエクスポートする。

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
        arg: argument.TwitterFollowxxExportArg = argument.TwitterFollowxxExportArg(arg_namespace)
        __validate_arg(arg)

        # ロジック(TwitterAPI認証)の実行
        api: tweepy.API = twitter_api_auth.do_logic_that_generate_api_by_oauth_1_user()

        # ロジック(Twitterフォロイー(フォロワー)エクスポート)の実行
        if bool(arg.export_followee) is True:
            # ロジック(Twitterフォロイーエクスポート)の実行
            twitter_followxx_export.do_logic(
                api,
                twitter_followxx_export.EnumOfProc.EXPORT_FOLLOWEE,
                arg.user_id,
                arg.num_of_followxxs,
            )
        elif bool(arg.export_follower) is True:
            # ロジック(Twitterフォロワーエクスポート)の実行
            twitter_followxx_export.do_logic(
                api,
                twitter_followxx_export.EnumOfProc.EXPORT_FOLLOWER,
                arg.user_id,
                arg.num_of_followxxs,
            )
    except Exception as e:
        raise (e)

    return None


def __validate_arg(arg: argument.TwitterFollowxxExportArg) -> None:
    """引数検証"""

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__)

        # 引数指定の確認
        if arg.is_specified() is False:
            raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

        # 検証：ユーザIDが4文字以上であること
        if not (len(arg.user_id) >= 4):
            raise pyl.ArgumentValidationError(f"ユーザIDが4文字以上ではありません。(user_id:{arg.user_id})")

        # 検証：フォロイー(フォロワー)数が1人以上であること
        if not (arg.num_of_followxxs >= 1):
            raise pyl.ArgumentValidationError(
                f"フォロイー(フォロワー)数が1人以上ではありません。(num_of_followxxs:{arg.num_of_followxxs})"
            )
    except Exception as e:
        raise (e)

    return None

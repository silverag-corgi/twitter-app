import argparse
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
        # 引数の取得
        arg: argument.TwitterFollowxxExportArg = argument.TwitterFollowxxExportArg(arg_namespace)

        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=arg.use_debug_mode)
        clg.log_inf(f"Twitterフォロイー(フォロワー)エクスポートを開始します。")

        # ロジック(TwitterAPI認証)の実行
        api: tweepy.API = twitter_api_auth.do_logic_that_generate_api_by_oauth_1_user(
            arg.use_debug_mode
        )

        # ロジック(Twitterフォロイー(フォロワー)エクスポート)の実行
        if arg.export_followee is True:
            # ロジック(Twitterフォロイーエクスポート)の実行
            twitter_followxx_export.do_logic(
                arg.use_debug_mode,
                api,
                twitter_followxx_export.EnumOfProc.EXPORT_FOLLOWEE,
                arg.user_id,
                arg.num_of_followxxs,
            )
        elif arg.export_follower is True:
            # ロジック(Twitterフォロワーエクスポート)の実行
            twitter_followxx_export.do_logic(
                arg.use_debug_mode,
                api,
                twitter_followxx_export.EnumOfProc.EXPORT_FOLLOWER,
                arg.user_id,
                arg.num_of_followxxs,
            )
    except Exception as e:
        raise (e)
    finally:
        if clg is not None:
            clg.log_inf(f"Twitterフォロイー(フォロワー)エクスポートを終了します。")

    return None

import argparse
from typing import Optional

import pandas as pd
import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth, twitter_list_export, twitter_list_show
from twitter_app.main import argument


def export_twitter_list(arg_namespace: argparse.Namespace) -> None:
    """
    Twitterリストエクスポート

    Summary:
        引数を検証して問題ない場合、指定したリストをTwitterからエクスポートする。

    Args:
        arg_namespace (argparse.Namespace): 引数名前空間

    Returns:
        None
    """

    clg: Optional[pyl.CustomLogger] = None

    try:
        # 引数の取得
        arg: argument.TwitterListExportArg = argument.TwitterListExportArg(arg_namespace)

        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=arg.use_debug_mode)

        # 引数の検証
        __validate_arg(arg)

        # ロジック(TwitterAPI認証)の実行
        api: tweepy.API = twitter_api_auth.do_logic_that_generate_api_by_oauth_1_user(
            arg.use_debug_mode,
        )

        # ロジック(Twitterリスト表示)の実行
        list_df: pd.DataFrame = pd.DataFrame()
        if bool(arg.all_list) is True:
            list_df = twitter_list_show.do_logic(
                arg.use_debug_mode,
                api,
                twitter_list_show.EnumOfProcTargetList.ALL,
                "",
            )
        elif arg.list_id is not None:
            list_df = twitter_list_show.do_logic(
                arg.use_debug_mode,
                api,
                twitter_list_show.EnumOfProcTargetList.ID,
                arg.list_id,
            )
        elif arg.list_name is not None:
            list_df = twitter_list_show.do_logic(
                arg.use_debug_mode,
                api,
                twitter_list_show.EnumOfProcTargetList.NAME,
                arg.list_name,
            )

        # ロジック(Twitterリストエクスポート)の実行
        twitter_list_export.do_logic(arg.use_debug_mode, api, list_df)
    except Exception as e:
        raise (e)

    return None


def __validate_arg(arg: argument.TwitterListExportArg) -> None:
    """引数検証"""

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=arg.use_debug_mode)

        # 引数指定の確認
        if arg.is_specified() is False:
            raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

        # 検証：グループBの引数が指定された場合は1文字以上であること
        if arg.list_id is not None and not (len(arg.list_id) >= 1):
            raise pyl.ArgumentValidationError(f"リストIDが1文字以上ではありません。(list_id:{arg.list_id})")
        elif arg.list_name is not None and not (len(arg.list_name) >= 1):
            raise pyl.ArgumentValidationError(f"リスト名が1文字以上ではありません。(list_name:{arg.list_name})")
    except Exception as e:
        raise (e)

    return None

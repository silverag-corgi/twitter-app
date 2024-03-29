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
        clg.log_inf(f"Twitterリストエクスポートを開始します。")

        # ロジック(TwitterAPI認証)の実行
        api: tweepy.API = twitter_api_auth.do_logic_that_generate_api_by_oauth_1_user(
            arg.use_debug_mode,
        )

        # ロジック(Twitterリスト表示)の実行
        list_df: pd.DataFrame = pd.DataFrame()
        if arg.all_list is True:
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
    finally:
        if clg is not None:
            clg.log_inf(f"Twitterリストエクスポートを終了します。")

    return None

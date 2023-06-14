import argparse
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth, twitter_list_show
from twitter_app.main import argument


def show_twitter_list(arg_namespace: argparse.Namespace) -> None:
    """
    Twitterリスト表示

    Summary:
        引数を検証して問題ない場合、指定したリストを表示する。

    Args:
        arg_namespace (argparse.Namespace): 引数名前空間

    Returns:
        None
    """

    clg: Optional[pyl.CustomLogger] = None

    try:
        # 引数の取得
        arg: argument.TwitterListShowArg = argument.TwitterListShowArg(arg_namespace)

        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=arg.use_debug_mode)
        clg.log_inf(f"Twitterリスト表示を開始します。")

        # ロジック(TwitterAPI認証)の実行
        api: tweepy.API = twitter_api_auth.do_logic_that_generate_api_by_oauth_1_user(
            arg.use_debug_mode,
        )

        # ロジック(Twitterリスト表示)の実行
        if arg.all_list is True:
            twitter_list_show.do_logic(
                arg.use_debug_mode,
                api,
                twitter_list_show.EnumOfProcTargetList.ALL,
                "",
            )
        elif arg.list_id is not None:
            twitter_list_show.do_logic(
                arg.use_debug_mode,
                api,
                twitter_list_show.EnumOfProcTargetList.ID,
                arg.list_id,
            )
        elif arg.list_name is not None:
            twitter_list_show.do_logic(
                arg.use_debug_mode,
                api,
                twitter_list_show.EnumOfProcTargetList.NAME,
                arg.list_name,
            )
    except Exception as e:
        raise (e)
    finally:
        if clg is not None:
            clg.log_inf(f"Twitterリスト表示を終了します。")

    return None

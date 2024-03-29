import argparse
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth, twitter_list_import
from twitter_app.main import argument


def import_twitter_list(arg_namespace: argparse.Namespace) -> None:
    """
    Twitterリストインポート

    Summary:
        引数を検証して問題ない場合、指定したcsvファイルをリストとしてTwitterにインポートする。

    Args:
        arg_namespace (argparse.Namespace): 引数名前空間

    Returns:
        None
    """

    clg: Optional[pyl.CustomLogger] = None

    try:
        # 引数の取得
        arg: argument.TwitterListImportArg = argument.TwitterListImportArg(arg_namespace)

        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=arg.use_debug_mode)
        clg.log_inf(f"Twitterリストインポートを開始します。")

        # ロジック(TwitterAPI認証)の実行
        api: tweepy.API = twitter_api_auth.do_logic_that_generate_api_by_oauth_1_user(
            arg.use_debug_mode,
        )

        # ロジック(Twitterリストインポート)の実行
        twitter_list_import.do_logic(
            arg.use_debug_mode,
            api,
            arg.list_member_file_path,
            arg.header_line_num,
            arg.add_only_users_with_diff,
        )
    except Exception as e:
        raise (e)
    finally:
        if clg is not None:
            clg.log_inf(f"Twitterリストインポートを終了します。")

    return None

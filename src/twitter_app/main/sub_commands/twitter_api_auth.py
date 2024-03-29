import argparse
from typing import Optional

import python_lib_for_me as pyl

from twitter_app.logic import twitter_api_auth
from twitter_app.main import argument


def authenticate_twitter_api(arg_namespace: argparse.Namespace) -> None:
    """
    TwitterAPI認証

    Summary:
        コンシューマーキーとPINコードを基にアクセストークンを生成し、認証情報ファイルに保存する。

    Args:
        arg_namespace (argparse.Namespace): 引数名前空間

    Returns:
        None
    """

    clg: Optional[pyl.CustomLogger] = None

    try:
        # 引数の取得
        arg: argument.TwitterApiAuthArg = argument.TwitterApiAuthArg(arg_namespace)

        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=arg.use_debug_mode)
        clg.log_inf(f"TwitterAPI認証を開始します。")

        # ロジック(TwitterAPI認証)の実行
        twitter_api_auth.do_logic_that_generate_api_by_oauth_1_user_using_pin(
            arg.use_debug_mode,
        )
    except Exception as e:
        raise (e)
    finally:
        if clg is not None:
            clg.log_inf(f"TwitterAPI認証を終了します。")

    return None

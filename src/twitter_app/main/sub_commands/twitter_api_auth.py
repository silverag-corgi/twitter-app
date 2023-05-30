import argparse
import os
import sys
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
        # ロガーの取得
        clg = pyl.CustomLogger(__name__)

        # 引数の検証
        arg: argument.TwitterApiAuthArg = argument.TwitterApiAuthArg(arg_namespace)
        __validate_arg(arg)

        # ロジック(TwitterAPI認証)の実行
        twitter_api_auth.do_logic_that_generate_api_by_oauth_1_user_using_pin()
    except Exception as e:
        raise (e)

    return None


def __validate_arg(arg: argument.TwitterApiAuthArg) -> None:
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

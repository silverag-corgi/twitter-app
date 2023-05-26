import argparse
import os
import sys
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth
from twitter_app.util.twitter_api_v1_1.standard import twitter_developer_util


def main() -> int:
    """
    メイン

    Summary:
        コマンドラインから実行する。

        引数を検証して問題ない場合、指定したリソース群とエンドポイントのレート制限を表示する。

    Args:
        -

    Args on cmd line:
        resource_family (str)   : [グループA][必須] リソース群
        endpoint (str)          : [グループA][必須] エンドポイント

    Returns:
        int: 終了コード(0：正常、1：異常)
    """

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__)

        # 実行コマンドの表示
        sys.argv[0] = os.path.basename(sys.argv[0])
        clg.log_inf(f"実行コマンド：{sys.argv}")

        # 引数の取得・検証
        args: argparse.Namespace = __get_args()
        if __validate_args(args) is False:
            return 1

        # ロジック(TwitterAPI認証)の実行
        api: tweepy.API = twitter_api_auth.do_logic_that_generate_api_by_oauth_1_user()

        # レート制限の表示
        twitter_developer_util.show_rate_limit(api, args.resource_family, args.endpoint)
    except KeyboardInterrupt as e:
        if clg is not None:
            clg.log_inf(f"処理を中断しました。")
    except Exception as e:
        if clg is not None:
            clg.log_exc("")
        return 1

    return 0


def __get_args() -> argparse.Namespace:
    """引数取得"""

    try:
        parser: pyl.CustomArgumentParser = pyl.CustomArgumentParser(
            description="Twitterレート制限表示\n" + "指定したリソース群とエンドポイントのレート制限を表示します",
            formatter_class=argparse.RawTextHelpFormatter,
            exit_on_error=True,
        )

        help_: str = ""

        # グループAの引数(全て必須な引数)
        arg_group_a: argparse._ArgumentGroup = parser.add_argument_group(
            "Group A - all required arguments",
            "全て必須な引数\n" + "表示するレート制限を指定します\n" + "両方とも空文字の場合は全てのレート制限を表示します",
        )
        help_ = "リソース群\n" + "例：friends"
        arg_group_a.add_argument("resource_family", type=str, help=help_)
        help_ = "エンドポイント\n" + "例：/friends/list"
        arg_group_a.add_argument("endpoint", type=str, help=help_)

        args: argparse.Namespace = parser.parse_args()
    except Exception as e:
        raise (e)

    return args


def __validate_args(args: argparse.Namespace) -> bool:
    """引数検証"""

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__)

        # 検証：なし
    except Exception as e:
        raise (e)

    return True


if __name__ == "__main__":
    sys.exit(main())

import argparse
import os
import sys
from typing import Optional

import pandas as pd
import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth, twitter_list_export, twitter_list_show


def main() -> int:
    """
    メイン

    Summary:
        コマンドラインから実行する。

        引数を検証して問題ない場合、指定したリストをTwitterからエクスポートする。

    Args:
        -

    Args on cmd line:
        all_list (bool) : [グループB][1つのみ必須] 全てのリスト
        list_id (str)   : [グループB][1つのみ必須] リストID(csv形式)
        list_name (str) : [グループB][1つのみ必須] リスト名(csv形式)

    Returns:
        int: 終了コード(0：正常、1：異常)

    Destinations:
        リストメンバーファイル: ./dest/list_member/[リスト名].csv
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
        __validate_args(args)

        # ロジック(TwitterAPI認証)の実行
        api: tweepy.API = twitter_api_auth.do_logic_that_generate_api_by_oauth_1_user()

        # ロジック(Twitterリスト表示)の実行
        list_df: pd.DataFrame = pd.DataFrame()
        if bool(args.all_list) is True:
            list_df = twitter_list_show.do_logic(
                api, twitter_list_show.EnumOfProcTargetList.ALL, ""
            )
        elif args.list_id is not None:
            list_df = twitter_list_show.do_logic(
                api, twitter_list_show.EnumOfProcTargetList.ID, args.list_id
            )
        elif args.list_name is not None:
            list_df = twitter_list_show.do_logic(
                api, twitter_list_show.EnumOfProcTargetList.NAME, args.list_name
            )

        # ロジック(Twitterリストエクスポート)の実行
        twitter_list_export.do_logic(api, list_df)
    except KeyboardInterrupt as e:
        if clg is not None:
            clg.log_inf(f"処理を中断しました。")
        return 1
    except pyl.ArgumentValidationError as e:
        if clg is not None:
            clg.log_err(f"{e}")
        return 1
    except Exception as e:
        if clg is not None:
            clg.log_exc("")
        return 1

    return 0


def __get_args() -> argparse.Namespace:
    """引数取得"""

    try:
        parser: pyl.CustomArgumentParser = pyl.CustomArgumentParser(
            description="Twitterリストエクスポート\n" + "指定したリストをTwitterからエクスポートします",
            formatter_class=argparse.RawTextHelpFormatter,
            exit_on_error=True,
        )

        help_: str = ""

        # グループBの引数(1つのみ必須な引数)
        arg_group_b: argparse._ArgumentGroup = parser.add_argument_group(
            "Group B - only one required arguments", "1つのみ必須な引数\n処理対象のリストを指定します"
        )
        mutually_exclusive_group_b: argparse._MutuallyExclusiveGroup = (
            arg_group_b.add_mutually_exclusive_group(required=True)
        )
        help_ = "{0}\n{1}"
        mutually_exclusive_group_b.add_argument(
            "-all", "--all_list", action="store_true", help=help_.format("全てのリスト", "")
        )
        mutually_exclusive_group_b.add_argument(
            "-id",
            "--list_id",
            type=str,
            help=help_.format("リストID(csv形式)", '例："0123456789111111111, 0123456789222222222"'),
        )
        mutually_exclusive_group_b.add_argument(
            "-name",
            "--list_name",
            type=str,
            help=help_.format("リスト名(csv形式)", '例："Google関連, Microsoft関連"'),
        )

        args: argparse.Namespace = parser.parse_args()
    except Exception as e:
        raise (e)

    return args


def __validate_args(args: argparse.Namespace) -> None:
    """引数検証"""

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__)

        # 検証：グループBの引数が指定された場合は1文字以上であること
        if args.list_id is not None and not (len(args.list_id) >= 1):
            raise pyl.ArgumentValidationError(f"リストIDが1文字以上ではありません。(list_id:{args.list_id})")
        elif args.list_name is not None and not (len(args.list_name) >= 1):
            raise pyl.ArgumentValidationError(f"リスト名が1文字以上ではありません。(list_name:{args.list_name})")
    except Exception as e:
        raise (e)

    return None


if __name__ == "__main__":
    sys.exit(main())

import argparse
import os
import sys
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth, twitter_list_import


def main() -> int:
    """
    メイン

    Summary:
        コマンドラインから実行する。

        引数を検証して問題ない場合、指定したcsvファイルをリストとしてTwitterにインポートする。

    Args:
        -

    Args on cmd line:
        list_member_file_path (str)     : [グループC][任意] リストメンバーファイルパス(csvファイル)
        header_line_num (int)           : [グループC][任意] ヘッダ行番号
        add_only_users_with_diff (bool) : [グループC][任意] 差分ユーザ追加

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
        __validate_args(args)

        # ロジック(TwitterAPI認証)の実行
        api: tweepy.API = twitter_api_auth.do_logic_that_generate_api_by_oauth_1_user()

        # ロジック(Twitterリストインポート)の実行
        twitter_list_import.do_logic(
            api,
            args.list_member_file_path,
            int(args.header_line_num),
            args.add_only_users_with_diff,
        )
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
            description="Twitterリストインポート\n" + "指定したcsvファイルをリストとしてTwitterにインポートします",
            formatter_class=argparse.RawTextHelpFormatter,
            exit_on_error=True,
        )

        help_: str = ""

        # グループCの引数(任意の引数)
        arg_group_c: argparse._ArgumentGroup = parser.add_argument_group(
            "Group C - optional arguments", "任意の引数"
        )
        help_ = "リストメンバーファイルパス(csvファイル) (デフォルト：%(default)s)\n" + "ワイルドカード可"
        arg_group_c.add_argument(
            "-l", "--list_member_file_path", type=str, default="input/list_member/*.csv", help=help_
        )
        help_ = "ヘッダ行番号 (デフォルト：%(default)s)\n" + "0：ヘッダなし、1~：ヘッダとなるファイルの行番号"
        arg_group_c.add_argument("-hd", "--header_line_num", type=int, default="1", help=help_)
        help_ = (
            "差分ユーザ追加\n" + "指定した場合は既存のリストに差分のあるユーザのみを追加します\n" + "指定しない場合は既存のリストを削除して新しいリストにユーザを追加します"
        )
        arg_group_c.add_argument(
            "-d", "--add_only_users_with_diff", action="store_true", help=help_
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

        # 検証：リストメンバーファイルパスがcsvファイルのパスであること
        list_member_file_path_and_ext: tuple[str, str] = os.path.splitext(
            args.list_member_file_path
        )
        if not (list_member_file_path_and_ext[1] == ".csv"):
            raise pyl.ArgumentValidationError(
                f"リストメンバーファイルパスがcsvファイルのパスではありません。(list_member_file_path:{args.list_member_file_path})"
            )

        # 検証：ヘッダ行番号が0以上であること
        if not (int(args.header_line_num) >= 0):
            raise pyl.ArgumentValidationError(
                f"ヘッダ行番号が0以上ではありません。(header_line_num:{args.header_line_num})"
            )
    except Exception as e:
        raise (e)

    return None


if __name__ == "__main__":
    sys.exit(main())

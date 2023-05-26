import argparse
import os
import sys
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth, twitter_tweet_stream


def main() -> int:
    """
    メイン

    Summary:
        コマンドラインから実行する。

        引数を検証して問題ない場合、指定したキーワードのツイートを配信する。

    Args:
        -

    Args on cmd line:
        user_id_for_followees (str)     : [グループB][1つのみ必須] ユーザID(フォロイー用)
        list_id (str)                   : [グループB][1つのみ必須] リストID
        list_name (str)                 : [グループB][1つのみ必須] リスト名
        following_user_file_path (str)  : [グループB][1つのみ必須] フォローユーザファイルパス(csvファイル)、ヘッダ行番号
        keyword_of_csv_format (str)     : [グループC][任意] キーワード(csv形式)

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

        # ロジック(Twitterツイート配信)の実行
        if args.user_id_for_followees is not None:
            twitter_tweet_stream.do_logic(
                api,
                twitter_tweet_stream.EnumOfProcTargetItem.USER_ID,
                args.user_id_for_followees,
                args.keyword_of_csv_format,
            )
        elif args.list_id is not None:
            twitter_tweet_stream.do_logic(
                api,
                twitter_tweet_stream.EnumOfProcTargetItem.LIST_ID,
                args.list_id,
                args.keyword_of_csv_format,
            )
        elif args.list_name is not None:
            twitter_tweet_stream.do_logic(
                api,
                twitter_tweet_stream.EnumOfProcTargetItem.LIST_NAME,
                args.list_name,
                args.keyword_of_csv_format,
            )
        elif args.following_user_file_path is not None:
            twitter_tweet_stream.do_logic(
                api,
                twitter_tweet_stream.EnumOfProcTargetItem.FILE_PATH,
                args.following_user_file_path[0],
                args.keyword_of_csv_format,
                int(args.following_user_file_path[1]),
            )
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
            description="Twitterツイート配信\n" + "指定したキーワードのツイートを配信します",
            formatter_class=argparse.RawTextHelpFormatter,
            exit_on_error=True,
        )

        help_: str = ""

        # グループBの引数(1つのみ必須な引数)
        arg_group_b: argparse._ArgumentGroup = parser.add_argument_group(
            "Group B - only one required arguments", "1つのみ必須な引数\n処理対象の項目を指定します"
        )
        mutually_exclusive_group_a: argparse._MutuallyExclusiveGroup = (
            arg_group_b.add_mutually_exclusive_group(required=True)
        )
        help_ = "{0}\n" + "{1}のツイートを配信します"
        mutually_exclusive_group_a.add_argument(
            "-ui",
            "--user_id_for_followees",
            type=str,
            help=help_.format("ユーザID(フォロイー用)", "指定したユーザIDのフォロイー"),
        )
        mutually_exclusive_group_a.add_argument(
            "-li", "--list_id", type=str, help=help_.format("リストID", "指定したリストID")
        )
        mutually_exclusive_group_a.add_argument(
            "-ln", "--list_name", type=str, help=help_.format("リスト名", "指定したリスト名")
        )
        help_ = "{0} {1}\n" + "{2}のツイートを配信します\n" + "{3}"
        mutually_exclusive_group_a.add_argument(
            "-fp",
            "--following_user_file_path",
            type=str,
            nargs=2,
            help=help_.format(
                "フォローユーザファイルパス(csvファイル)",
                "ヘッダ行番号",
                "指定したファイルに記載されているユーザ",
                "ヘッダ行番号は 0：ヘッダなし 1~：ヘッダとなるファイルの行番号 です",
            ),
            metavar=("FILE_PATH", "HEADER_LINE_NUM"),
        )

        # グループCの引数(任意の引数)
        arg_group_c: argparse._ArgumentGroup = parser.add_argument_group(
            "Group C - optional arguments", "任意の引数"
        )
        help_ = (
            "キーワード(csv形式)\n"
            + '例："Google Docs, Google Drive"\n'
            + "スペースはAND検索(Google AND Docs)\n"
            + "カンマはOR検索(Google Docs OR Google Drive)"
        )
        arg_group_c.add_argument("-k", "--keyword_of_csv_format", type=str, default="", help=help_)

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

        # 検証：グループAの引数が指定された場合は1文字以上であること
        if args.user_id_for_followees is not None and not (len(args.user_id_for_followees) >= 1):
            clg.log_err(
                f"ユーザID(フォロイー用)が1文字以上ではありません。(user_id_for_followees:{args.user_id_for_followees})",
            )
            return False
        elif args.list_id is not None and not (len(args.list_id) >= 1):
            clg.log_err(f"リストIDが1文字以上ではありません。(list_id:{args.list_id})")
            return False
        elif args.list_name is not None and not (len(args.list_name) >= 1):
            clg.log_err(f"リスト名が1文字以上ではありません。(list_name:{args.list_name})")
            return False
        elif args.following_user_file_path is not None and not (
            len(args.following_user_file_path[0]) >= 1
        ):
            clg.log_err(
                f"フォローユーザファイルパスが1文字以上ではありません。(following_user_file_path[0]:{args.following_user_file_path[0]})",
            )
            return False

        # 検証：フォローユーザファイルパスがcsvファイルのパスであること
        if args.following_user_file_path is not None and not (
            os.path.splitext(args.following_user_file_path[0])[1] == ".csv"
        ):
            clg.log_err(
                f"フォローユーザファイルパスがcsvファイルのパスではありません。(following_user_file_path[0]:{args.following_user_file_path[0]})",
            )
            return False

        # 検証：フォローユーザファイルパスのファイルが存在すること
        if args.following_user_file_path is not None and not (
            os.path.isfile(args.following_user_file_path[0]) is True
        ):
            clg.log_err(
                f"フォローユーザファイルパスのファイルが存在しません。(following_user_file_path[0]:{args.following_user_file_path[0]})",
            )
            return False

        # 検証：ヘッダ行番号が0以上であること
        if not (args.following_user_file_path[1].isdecimal() is True):
            clg.log_err(
                f"ヘッダ行番号が0以上ではありません。(following_user_file_path[1]:{args.following_user_file_path[1]})",
            )
            return False
    except Exception as e:
        raise (e)

    return True


if __name__ == "__main__":
    sys.exit(main())

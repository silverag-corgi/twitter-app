import argparse
import os
import sys
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth, twitter_tweet_search


def main() -> int:
    """
    メイン

    Summary:
        コマンドラインから実行する。

        引数を検証して問題ない場合、指定したクエリでツイートを検索し、ツイート検索結果ファイルを生成する。

    Args:
        -

    Args on cmd line:
        query (str)             : [グループA][必須] クエリ
        num_of_tweets (int)     : [グループC][任意] ツイート数(デフォルト：18000)

    Returns:
        int: 終了コード(0：正常、1：異常)

    Destinations:
        ツイート検索結果ファイル: ./dest/tweet_search_result/[クエリ].csv
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

        # ロジック(Twitterツイート検索)の実行
        twitter_tweet_search.do_logic(api, args.query, args.num_of_tweets)
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
            description="Twitterツイート検索\n" + "指定したクエリでツイートを検索し、ツイート検索結果ファイルを生成します",
            formatter_class=argparse.RawTextHelpFormatter,
            exit_on_error=True,
        )

        help_: str = ""

        # グループAの引数(全て必須な引数)
        arg_group_a: argparse._ArgumentGroup = parser.add_argument_group(
            "Group A - all required arguments", "全て必須な引数"
        )
        help_ = "クエリ\n" + "RTと返信はデフォルトで除外します"
        arg_group_a.add_argument("query", help=help_)

        # グループCの引数(任意の引数)
        arg_group_c: argparse._ArgumentGroup = parser.add_argument_group(
            "Group C - optional arguments", "任意の引数"
        )
        help_ = (
            "ツイート数 (デフォルト：%(default)s)\n"
            + "表示するツイートの数\n"
            + "18000件を超過した場合はレート制限により18000件ごとに15分の待機時間が発生します"
        )
        arg_group_c.add_argument("-t", "--num_of_tweets", type=int, default=100, help=help_)

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

        # 検証：クエリが1文字以上であること
        if not (len(args.query) >= 1):
            clg.log_err(f"クエリが1文字以上ではありません。(query:{args.query})")
            return False

        # 検証：ツイート数が1件以上であること
        if not (int(args.num_of_tweets) >= 1):
            clg.log_err(f"ツイート数が1件以上ではありません。(num_of_tweets:{args.num_of_tweets})")
            return False
    except Exception as e:
        raise (e)

    return True


if __name__ == "__main__":
    sys.exit(main())

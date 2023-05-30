import argparse
import os
import sys
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth, twitter_tweet_stream
from twitter_app.main import argument


def stream_twitter_tweet(arg_namespace: argparse.Namespace) -> None:
    """
    Twitterツイート配信

    Summary:
        引数を検証して問題ない場合、指定したキーワードのツイートを配信する。

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
        arg: argument.TwitterTweetStreamArg = argument.TwitterTweetStreamArg(arg_namespace)
        __validate_arg(arg)

        # ロジック(TwitterAPI認証)の実行
        api: tweepy.API = twitter_api_auth.do_logic_that_generate_api_by_oauth_1_user()

        # ロジック(Twitterツイート配信)の実行
        if arg.user_id_for_followees is not None:
            twitter_tweet_stream.do_logic(
                api,
                twitter_tweet_stream.EnumOfProcTargetItem.USER_ID,
                arg.user_id_for_followees,
                arg.keyword_of_csv_format,
            )
        elif arg.list_id is not None:
            twitter_tweet_stream.do_logic(
                api,
                twitter_tweet_stream.EnumOfProcTargetItem.LIST_ID,
                arg.list_id,
                arg.keyword_of_csv_format,
            )
        elif arg.list_name is not None:
            twitter_tweet_stream.do_logic(
                api,
                twitter_tweet_stream.EnumOfProcTargetItem.LIST_NAME,
                arg.list_name,
                arg.keyword_of_csv_format,
            )
        elif arg.following_user_file_path is not None:
            twitter_tweet_stream.do_logic(
                api,
                twitter_tweet_stream.EnumOfProcTargetItem.FILE_PATH,
                arg.following_user_file_path[0],
                arg.keyword_of_csv_format,
                int(arg.following_user_file_path[1]),
            )
    except Exception as e:
        raise (e)

    return None


def __validate_arg(arg: argument.TwitterTweetStreamArg) -> None:
    """引数検証"""

    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__)

        # 引数指定の確認
        if arg.is_specified() is False:
            raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

        # 検証：グループAの引数が指定された場合は1文字以上であること
        if arg.user_id_for_followees is not None and not (len(arg.user_id_for_followees) >= 1):
            raise pyl.ArgumentValidationError(
                f"ユーザID(フォロイー用)が1文字以上ではありません。(user_id_for_followees:{arg.user_id_for_followees})",
            )
        elif arg.list_id is not None and not (len(arg.list_id) >= 1):
            raise pyl.ArgumentValidationError(f"リストIDが1文字以上ではありません。(list_id:{arg.list_id})")
        elif arg.list_name is not None and not (len(arg.list_name) >= 1):
            raise pyl.ArgumentValidationError(f"リスト名が1文字以上ではありません。(list_name:{arg.list_name})")
        elif arg.following_user_file_path is not None and not (
            len(arg.following_user_file_path[0]) >= 1
        ):
            raise pyl.ArgumentValidationError(
                f"フォローユーザファイルパスが1文字以上ではありません。(following_user_file_path[0]:{arg.following_user_file_path[0]})",
            )

        # 検証：フォローユーザファイルパスがcsvファイルのパスであること
        if arg.following_user_file_path is not None and not (
            os.path.splitext(arg.following_user_file_path[0])[1] == ".csv"
        ):
            raise pyl.ArgumentValidationError(
                f"フォローユーザファイルパスがcsvファイルのパスではありません。(following_user_file_path[0]:{arg.following_user_file_path[0]})",
            )

        # 検証：フォローユーザファイルパスのファイルが存在すること
        if arg.following_user_file_path is not None and not (
            os.path.isfile(arg.following_user_file_path[0]) is True
        ):
            raise pyl.ArgumentValidationError(
                f"フォローユーザファイルパスのファイルが存在しません。(following_user_file_path[0]:{arg.following_user_file_path[0]})",
            )

        # 検証：ヘッダ行番号が0以上であること
        if arg.following_user_file_path is not None and not (
            str(arg.following_user_file_path[1]).isdecimal() is True
        ):
            raise pyl.ArgumentValidationError(
                f"ヘッダ行番号が0以上ではありません。(following_user_file_path[1]:{arg.following_user_file_path[1]})",
            )
    except Exception as e:
        raise (e)

    return None

import argparse
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
        # 引数の取得
        arg: argument.TwitterTweetStreamArg = argument.TwitterTweetStreamArg(arg_namespace)

        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=arg.use_debug_mode)
        clg.log_inf(f"Twitterツイート配信を開始します。")

        # ロジック(TwitterAPI認証)の実行
        api: tweepy.API = twitter_api_auth.do_logic_that_generate_api_by_oauth_1_user(
            arg.use_debug_mode,
        )

        # ロジック(Twitterツイート配信)の実行
        if arg.user_id_for_followees is not None:
            twitter_tweet_stream.do_logic(
                arg.use_debug_mode,
                api,
                twitter_tweet_stream.EnumOfProcTargetItem.USER_ID,
                arg.user_id_for_followees,
                arg.keyword_of_csv_format,
            )
        elif arg.list_id is not None:
            twitter_tweet_stream.do_logic(
                arg.use_debug_mode,
                api,
                twitter_tweet_stream.EnumOfProcTargetItem.LIST_ID,
                arg.list_id,
                arg.keyword_of_csv_format,
            )
        elif arg.list_name is not None:
            twitter_tweet_stream.do_logic(
                arg.use_debug_mode,
                api,
                twitter_tweet_stream.EnumOfProcTargetItem.LIST_NAME,
                arg.list_name,
                arg.keyword_of_csv_format,
            )
        elif arg.following_user_file_path is not None:
            twitter_tweet_stream.do_logic(
                arg.use_debug_mode,
                api,
                twitter_tweet_stream.EnumOfProcTargetItem.FILE_PATH,
                arg.following_user_file_path[0],
                arg.keyword_of_csv_format,
                int(arg.following_user_file_path[1]),
            )
    except Exception as e:
        raise (e)
    finally:
        if clg is not None:
            clg.log_inf(f"Twitterツイート配信を終了します。")

    return None

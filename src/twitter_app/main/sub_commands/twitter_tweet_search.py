import argparse
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth, twitter_tweet_search
from twitter_app.main import argument


def search_twitter_tweet(arg_namespace: argparse.Namespace) -> None:
    """
    Twitterツイート検索

    Summary:
        引数を検証して問題ない場合、指定したクエリでツイートを検索し、ツイート検索結果ファイルを生成する。

    Args:
        arg_namespace (argparse.Namespace): 引数名前空間

    Returns:
        None
    """

    clg: Optional[pyl.CustomLogger] = None

    try:
        # 引数の取得
        arg: argument.TwitterTweetSearchArg = argument.TwitterTweetSearchArg(arg_namespace)

        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=arg.use_debug_mode)
        clg.log_inf(f"Twitterツイート検索を開始します。")

        # ロジック(TwitterAPI認証)の実行
        api: tweepy.API = twitter_api_auth.do_logic_that_generate_api_by_oauth_1_user(
            arg.use_debug_mode,
        )

        # ロジック(Twitterツイート検索)の実行
        twitter_tweet_search.do_logic(
            arg.use_debug_mode,
            api,
            arg.query,
            arg.num_of_tweets,
        )
    except Exception as e:
        raise (e)
    finally:
        if clg is not None:
            clg.log_inf(f"Twitterツイート検索を終了します。")

    return None

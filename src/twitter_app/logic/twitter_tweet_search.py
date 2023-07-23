import os
import re
from typing import Optional

import pandas as pd
import python_lib_for_me as pyl
import tweepy
from tweepy.models import SearchResults

from twitter_app import util
from twitter_app.util import const_util, pandas_util
from twitter_app.util.twitter_api_v1_1.standard import twitter_developer_util, twitter_tweets_util


def do_logic(
    use_debug_mode: bool,
    api: tweepy.API,
    query: str,
    num_of_tweets: int,
) -> None:
    """ロジック実行"""

    clg: Optional[pyl.CustomLogger] = None
    tweet_search_result_file_path: str = ""

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=use_debug_mode)
        clg.log_inf(f"ロジック実行(Twitterツイート検索)を開始します。")

        # Pandasオプション設定
        pd.set_option("display.unicode.east_asian_width", True)

        # 想定処理時間の表示
        util.show_estimated_proc_time(
            use_debug_mode,
            num_of_tweets,
            twitter_tweets_util.EnumOfTweetsInPast7Day.EnumOfOauth1User.MAX_NUM_OF_DATA_PER_15MIN.value,
        )

        # レート制限の表示
        twitter_developer_util.show_rate_limit_of_search_tweets(use_debug_mode, api)

        # ツイート検索結果ページの取得
        query_with_filter: str = f"{query} -filter:replies -filter:retweets"
        tweet_search_result_pages: list[SearchResults] = twitter_tweets_util.search_tweets_in_past_7day(
            use_debug_mode,
            api,
            query_with_filter,
            twitter_tweets_util.EnumOfSearchResultType.RECENT,
            num_of_tweets,
        )

        # ツイート検索結果ページの件数が0件の場合
        if len(tweet_search_result_pages) == 0:
            clg.log_wrn(f"ツイート検索結果ページの件数が0件です。(query_with_filter:{query_with_filter})")
        else:
            # ツイート検索結果ファイルパスの生成
            query_for_name: str = re.sub(r'[\\/:*?"<>\|]+', "-", query)
            tweet_search_result_file_path = const_util.TWEET_SEARCH_RESULT_FILE_PATH.format(query_for_name)

            # ツイート検索結果データフレームの初期化
            tweet_search_result_df: pd.DataFrame = pd.DataFrame(columns=const_util.TWEET_SEARCH_RESULT_HEADER)

            # ツイート検索結果データフレームへの格納
            for tweets_by_page in tweet_search_result_pages:
                # tweet: tweepy.models.Status
                for tweet in tweets_by_page:
                    # ツイート情報データフレームの格納
                    tweet_info_df: pd.DataFrame = pd.DataFrame(
                        [
                            [
                                pyl.convert_timestamp_to_jst(str(tweet.created_at)),
                                tweet.user.screen_name,
                                tweet.user.name,
                                str(tweet.text).replace("\n", ""),
                                tweet.retweet_count,
                                tweet.favorite_count,
                                const_util.TWEET_URL.format(tweet.user.screen_name, tweet.id),
                            ]
                        ],
                        columns=const_util.TWEET_SEARCH_RESULT_HEADER,
                    )
                    tweet_search_result_df = pd.concat([tweet_search_result_df, tweet_info_df], ignore_index=True)

            # ツイート検索結果データフレームの保存
            clg.log_inf(f"ツイート検索結果(追加分先頭n行)：\n{tweet_search_result_df.head(5)}")
            clg.log_inf(f"ツイート検索結果(追加分末尾n行)：\n{tweet_search_result_df.tail(5)}")
            clg.log_inf(f"ツイート検索結果ファイルパス：\n{tweet_search_result_file_path}")
            pandas_util.save_tweet_search_result_df(
                use_debug_mode, tweet_search_result_df, tweet_search_result_file_path
            )

        # レート制限の表示
        twitter_developer_util.show_rate_limit_of_search_tweets(use_debug_mode, api)
    except Exception as e:
        # ツイート検索結果ファイルの削除
        if tweet_search_result_file_path != "" and os.path.isfile(tweet_search_result_file_path) is True:
            os.remove(tweet_search_result_file_path)

        raise (e)
    finally:
        if clg is not None:
            clg.log_inf(f"ロジック実行(Twitterツイート検索)を終了します。")

    return None

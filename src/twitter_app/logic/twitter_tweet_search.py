import math
import os
import re
from logging import Logger
from typing import Optional

import pandas as pd
import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet

from twitter_app import util
from twitter_app.util import const_util, pandas_util
from twitter_app.util.twitter_api_standard_v1_1 import twitter_developer_util, twitter_tweets_util


def do_logic(
        api: tweepy.API,
        query: str,
        num_of_tweets: int
    ) -> None:
    
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    tweet_search_result_path: str = ""
    
    try:
        # ロガー取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'Twitterツイート検索を開始します。')
        
        # Pandasオプション設定
        pd.set_option('display.unicode.east_asian_width', True)
        
        # 想定処理時間の表示
        util.show_estimated_proc_time(
                twitter_tweets_util.TWEETS_IN_PAST_7DAY.MAX_NUM_OF_DATA_PER_REQUEST.value,
                twitter_tweets_util.TWEETS_IN_PAST_7DAY.MAX_NUM_OF_REQUESTS_PER_15MIN.value,
                num_of_tweets
            )
        
        # レート制限の表示
        twitter_developer_util.show_rate_limit_of_search_tweets(api)
        
        # ツイート検索結果ページの取得
        query_with_filter: str = f'{query} -filter:replies -filter:retweets'
        tweet_search_result_pages: list[ResultSet] = twitter_tweets_util.search_tweets_in_past_7day(
                api,
                query_with_filter,
                twitter_tweets_util.SEARCH_RESULT_TYPE.RECENT,
                num_of_requests=math.ceil(
                    num_of_tweets /
                    twitter_tweets_util.TWEETS_IN_PAST_7DAY.MAX_NUM_OF_DATA_PER_REQUEST.value)
            )
        
        # ツイート検索結果ページの件数が0件の場合
        if len(tweet_search_result_pages) == 0:
            pyl.log_inf(lg, f'ツイート検索結果ページの件数が0件です。(query_with_filter:{query_with_filter})')
        else:
            # ツイート検索結果ファイル名の生成
            query_for_name: str = re.sub(r'[\\/:*?"<>\|]+', '-', query)
            tweet_search_result_path = \
                const_util.TWITTER_TWEET_SEARCH_RESULT_FILE_PATH.format(query_for_name)
            
            # ツイート検索結果データフレームの初期化
            tweet_search_result_df: pd.DataFrame = \
                pd.DataFrame(columns=const_util.TWITTER_TWEET_SEARCH_RESULT_HEADER)
            
            # ツイート検索結果データフレームへの格納
            for tweets_by_page in tweet_search_result_pages:
                # tweet: tweepy.models.SearchResults
                for tweet in tweets_by_page:
                    tweet_info_df: pd.DataFrame = pd.DataFrame(
                            [[
                                pyl.convert_timestamp_to_jst(str(tweet.created_at)),
                                tweet.user.screen_name,
                                tweet.user.name,
                                str(tweet.text).replace('\n', ''),
                                tweet.retweet_count,
                                tweet.favorite_count,
                                const_util.TWITTER_URL.format(tweet.user.screen_name, tweet.id)
                            ]],
                            columns=const_util.TWITTER_TWEET_SEARCH_RESULT_HEADER
                        )
                    
                    tweet_search_result_df = pd.concat(
                            [tweet_search_result_df, tweet_info_df],
                            ignore_index=True
                        )
            
            # ツイート検索結果データフレームの保存
            pyl.log_inf(lg, f'ツイート検索結果(追加分先頭n行)：\n{tweet_search_result_df.head(5)}')
            pyl.log_inf(lg, f'ツイート検索結果(追加分末尾n行)：\n{tweet_search_result_df.tail(5)}')
            pandas_util.save_tweet_search_result_df(
                tweet_search_result_df, tweet_search_result_path)
        
        # レート制限の表示
        twitter_developer_util.show_rate_limit_of_search_tweets(api)
        
        pyl.log_inf(lg, f'Twitterツイート検索を終了します。')
    except Exception as e:
        # ツイート検索結果ファイルの削除
        if tweet_search_result_path != '' \
            and os.path.isfile(tweet_search_result_path) == True:
            os.remove(tweet_search_result_path)
        raise(e)
    
    return None

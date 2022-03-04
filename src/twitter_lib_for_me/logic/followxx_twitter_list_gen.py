import math
from enum import IntEnum, auto
from logging import Logger
from typing import Any, Optional

import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet

from twitter_lib_for_me import util
from twitter_lib_for_me.util import const_util
from twitter_lib_for_me.util.twitter_api_standard_v1_1 import (
    twitter_developer_util,
    twitter_tweets_util,
    twitter_users_util,
)


class Pages(IntEnum):
    followee_list = auto()
    follower_list = auto()


def do_logic(api: tweepy.API, user_id: str, num_of_followxxs: int, kind_of_pages: Pages) -> None:
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    twitter_list: Optional[tweepy.List] = None
    
    try:
        # ロガー取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'フォロイー／フォロワーTwitterリスト生成を開始します。')
        
        # フォロイー／フォロワーの個別処理
        followxx_list_pages: list[ResultSet] = []
        twitter_list_name_format: str = ''
        if kind_of_pages == Pages.followee_list:
            # 想定処理時間の表示
            util.show_estimated_proc_time(
                    twitter_users_util.Followee.MAX_NUM_OF_DATA_PER_REQUEST,
                    twitter_users_util.Followee.MAX_NUM_OF_REQUESTS_PER_15MIN,
                    num_of_followxxs
                )
            
            # レート制限の表示
            twitter_developer_util.show_rate_limit_of_friends_list(api)
            
            # フォロイーリストページの取得
            followxx_list_pages = twitter_users_util.get_followee_list_pages(
                    api,
                    user_id,
                    num_of_requests=math.ceil(
                        num_of_followxxs / twitter_users_util.Followee.MAX_NUM_OF_DATA_PER_REQUEST)
                )
            
            # Twitterリスト名フォーマットの決定
            twitter_list_name_format = const_util.FOLLOWEE_TWITTER_LIST_NAME
        elif kind_of_pages == Pages.follower_list:
            # 想定処理時間の表示
            util.show_estimated_proc_time(
                    twitter_users_util.Follower.MAX_NUM_OF_DATA_PER_REQUEST,
                    twitter_users_util.Follower.MAX_NUM_OF_REQUESTS_PER_15MIN,
                    num_of_followxxs
                )
            
            # レート制限の表示
            twitter_developer_util.show_rate_limit_of_followers_list(api)
            
            # フォロワーリストページの取得
            followxx_list_pages = twitter_users_util.get_follower_list_pages(
                    api,
                    user_id,
                    num_of_requests=math.ceil(
                        num_of_followxxs / twitter_users_util.Follower.MAX_NUM_OF_DATA_PER_REQUEST)
                )
            
            # Twitterリスト名フォーマットの決定
            twitter_list_name_format = const_util.FOLLOWER_TWITTER_LIST_NAME
        
        # フォロイー／フォロワーのリストページの件数が0件の場合
        if len(followxx_list_pages) == 0:
            pyl.log_inf(lg, f'フォロイー／フォロワーのリストページの件数が0件です。(user_id:{user_id})')
        else:
            # Twitterリスト名の生成
            user_info: Any = twitter_users_util.get_user_info(api, user_id)
            twitter_list_name: str = \
                twitter_list_name_format.format(user_info.screen_name, user_info.name)
            
            # Twitterリストが存在しない場合
            if twitter_tweets_util.has_twitter_list(api, twitter_list_name) == False:
                # Twitterリストの生成
                twitter_list = twitter_tweets_util.generate_twitter_list(api, twitter_list_name)
                
                # フォロイー／フォロワーの取得・追加
                count_of_followxxs: int = 0
                count_of_added_followxxs: int = 0
                for page_index, followxxs_by_page in enumerate(followxx_list_pages, start=1):
                    # followxx: tweepy.models.User
                    for followxx_index, followxx in enumerate(followxxs_by_page, start=1):
                        # ユーザの追加
                        add_user_result: bool = twitter_tweets_util.add_user(
                                api,
                                twitter_list,
                                followxx.screen_name,
                                followxx.name
                            )
                        
                        # ユーザのカウント
                        count_of_followxxs = count_of_followxxs + 1
                        if add_user_result == True:
                            count_of_added_followxxs = count_of_added_followxxs + 1
                
                pyl.log_inf(lg, f'フォロイー／フォロワーの取得・追加が完了しました。' +
                            f'(count_of_followxxs:{count_of_added_followxxs}/{count_of_followxxs})')
                
                # Twitterリストの破棄(フォロイー／フォロワーが0人の場合)
                if count_of_added_followxxs == 0:
                    twitter_tweets_util.destroy_twitter_list(api, twitter_list)
        
        # レート制限の表示
        if kind_of_pages == Pages.followee_list:
            twitter_developer_util.show_rate_limit_of_friends_list(api)
        elif kind_of_pages == Pages.follower_list:
            twitter_developer_util.show_rate_limit_of_followers_list(api)
        
        pyl.log_inf(lg, f'フォロイー／フォロワーTwitterリスト生成を終了します。')
    except Exception as e:
        # Twitterリストの破棄
        if twitter_list is not None:
            twitter_tweets_util.destroy_twitter_list(api, twitter_list)
        
        raise(e)
    
    return None

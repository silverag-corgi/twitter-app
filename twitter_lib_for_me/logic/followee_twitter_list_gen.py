from logging import Logger
from typing import Any, Optional

import python_lib_for_me as mylib
import tweepy
from tweepy.models import ResultSet
from twitter_lib_for_me.util import const_util
from twitter_lib_for_me.util.twitter_api_standard_v1_1 import (
    twitter_developer_util, twitter_tweets_util, twitter_users_util)


def do_logic(api: tweepy.API, user_id: str) -> None:
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    twitter_list: Optional[tweepy.List] = None
    
    try:
        # ロガー取得
        lg = mylib.get_logger(__name__)
        lg.info(f'フォロイーTwitterリスト生成を開始します。')
        
        # レート制限の表示
        twitter_developer_util.show_rate_limit_of_friends_list(api)
        
        # フォロイーページの取得
        followee_pages: list[ResultSet] = twitter_users_util.get_followee_pages(
                api,
                user_id,
                max_num_of_data_per_request=200,
                num_of_requests_per_15min=15
            )
        
        # 実行要否の判定
        should_execute: bool = True
        if len(followee_pages) == 0:
            should_execute = False
            lg.info(f'フォロイーページの件数が0件です。(user_id:{user_id})')
        
        if should_execute == True:
            # Twitterリスト生成要否の判定
            should_generate: bool = True
            user: Any = api.get_user(screen_name=user_id) # user: tweepy.models.User
            twitter_list_name: str = \
                const_util.FOLLOWEE_TWITTER_LIST_NAME.format(user.screen_name, user.name)
            if twitter_tweets_util.has_twitter_list(api, twitter_list_name) == True:
                should_generate = False
            
            if should_generate == True:
                # Twitterリストの生成
                twitter_list = twitter_tweets_util.generate_twitter_list(api, twitter_list_name)
                
                # フォロイーの取得・追加
                num_of_followees: int = 0
                for page_index, followees_by_page in enumerate(followee_pages, start=1):
                    # followee: tweepy.models.User
                    for followee_index, followee in enumerate(followees_by_page, start=1):
                        num_of_followees = num_of_followees + 1
                        # lg.info(f'{num_of_followees:04d}, {page_index:04d}, {followee_index:04d}, ' +
                        #         f'{str(followee.protected): <5}, {followee.screen_name: <15}, ' +
                        #         f'{followee.name}')
                        twitter_tweets_util.add_user(
                                api,
                                twitter_list,
                                followee.screen_name,
                                followee.name
                            )
                lg.info(f'フォロイーの取得・追加が完了しました。(num_of_followees:{num_of_followees})')
                
                # Twitterリストの破棄(フォロイーが0人の場合)
                if num_of_followees == 0:
                    twitter_tweets_util.destroy_twitter_list(api, twitter_list)
        
        # レート制限の表示
        twitter_developer_util.show_rate_limit_of_friends_list(api)
        
        lg.info(f'フォロイーTwitterリスト生成を終了します。')
    except Exception as e:
        # Twitterリストの破棄
        if twitter_list is not None:
            twitter_tweets_util.destroy_twitter_list(api, twitter_list)
        
        raise(e)
    
    return None

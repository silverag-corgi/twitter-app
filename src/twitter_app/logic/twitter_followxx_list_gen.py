from enum import IntEnum, auto
from logging import Logger
from typing import Any, Optional

import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet

from twitter_app import util
from twitter_app.util import const_util
from twitter_app.util.twitter_api_v1_1.standard import twitter_developer_util, twitter_users_util


class EnumOfFollowxxList(IntEnum):
    FOLLOWEE_LIST = auto()
    FOLLOWER_LIST = auto()


def do_logic(
        api: tweepy.API,
        user_id: str,
        num_of_followxxs: int,
        enum_of_followxx_list: EnumOfFollowxxList
    ) -> None:
    
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    list_: Any = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'Twitterフォロイー(フォロワー)リスト生成を開始します。')
        
        # フォロイー(フォロワー)の個別処理
        followxx_pages: list[ResultSet] = []
        list_name_format: str = ''
        if enum_of_followxx_list == EnumOfFollowxxList.FOLLOWEE_LIST:
            # 想定処理時間の表示
            util.show_estimated_proc_time(
                    num_of_followxxs,
                    twitter_users_util.EnumOfFollowee.EnumOfOauth1User.
                    MAX_NUM_OF_DATA_PER_15MIN.value
                )
            
            # レート制限の表示
            twitter_developer_util.show_rate_limit_of_friends_list(api)
            
            # フォロイーページの取得
            followxx_pages = twitter_users_util.get_followee_pages(
                api, user_id, num_of_data=num_of_followxxs)
            
            # リスト名フォーマットの決定
            list_name_format = const_util.FOLLOWEE_LIST_NAME
        elif enum_of_followxx_list == EnumOfFollowxxList.FOLLOWER_LIST:
            # 想定処理時間の表示
            util.show_estimated_proc_time(
                    num_of_followxxs,
                    twitter_users_util.EnumOfFollower.EnumOfOauth1User.
                    MAX_NUM_OF_DATA_PER_15MIN.value
                )
            
            # レート制限の表示
            twitter_developer_util.show_rate_limit_of_followers_list(api)
            
            # フォロワーページの取得
            followxx_pages = twitter_users_util.get_follower_pages(
                api, user_id, num_of_data=num_of_followxxs)
            
            # リスト名フォーマットの決定
            list_name_format = const_util.FOLLOWER_LIST_NAME
        
        # フォロイー(フォロワー)のリストページの件数が0件の場合
        if len(followxx_pages) == 0:
            pyl.log_inf(lg, f'フォロイー(フォロワー)リストページの件数が0件です。' +
                            f'(user_id:{user_id})')
        else:
            # リスト名の生成
            user_info: Any = twitter_users_util.get_user_info(api, user_id)
            list_name: str = list_name_format.format(user_info.screen_name, user_info.name)
            
            # リストの破棄
            twitter_users_util.destroy_list(api, list_name)
            
            # リストの生成
            list_ = twitter_users_util.generate_list(api, list_name)
            
            # フォロイー(フォロワー)の追加
            twitter_users_util.add_users_to_list(
                    api,
                    list_.id,
                    [str(followxx.screen_name)
                        for followxxs_by_page in followxx_pages
                        for followxx in followxxs_by_page],
                    [str(followxx.name)
                        for followxxs_by_page in followxx_pages
                        for followxx in followxxs_by_page]
                )
        
        # レート制限の表示
        if enum_of_followxx_list == EnumOfFollowxxList.FOLLOWEE_LIST:
            twitter_developer_util.show_rate_limit_of_friends_list(api)
        elif enum_of_followxx_list == EnumOfFollowxxList.FOLLOWER_LIST:
            twitter_developer_util.show_rate_limit_of_followers_list(api)
        
        pyl.log_inf(lg, f'Twitterフォロイー(フォロワー)リスト生成を終了します。')
    except Exception as e:
        # リストの破棄
        if list_ is not None:
            twitter_users_util.destroy_list(api, list_.name)
        
        raise(e)
    
    return None

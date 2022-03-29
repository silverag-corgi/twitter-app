from enum import IntEnum, auto
from logging import Logger
from typing import Any, Optional

import pandas as pd
import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet

from twitter_app import util
from twitter_app.util import const_util, pandas_util
from twitter_app.util.twitter_api_v1_1.standard import twitter_developer_util, twitter_users_util


class EnumOfItemProcTarget(IntEnum):
    FOLLOWEE = auto()
    FOLLOWER = auto()


def do_logic(
        api: tweepy.API,
        user_id: str,
        num_of_followxxs: int,
        enum_of_item_proc_target: EnumOfItemProcTarget
    ) -> None:
    
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'Twitterフォロイー(フォロワー)エクスポートを開始します。')
        
        # Pandasオプション設定
        pd.set_option('display.unicode.east_asian_width', True)
        
        # フォロイー(フォロワー)の個別処理
        followxx_pages: list[ResultSet] = []
        followxx_file_path_format: str = ''
        if enum_of_item_proc_target == EnumOfItemProcTarget.FOLLOWEE:
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
            
            # フォロイーファイルパスフォーマットの決定
            followxx_file_path_format = const_util.FOLLOWEE_FILE_PATH
        elif enum_of_item_proc_target == EnumOfItemProcTarget.FOLLOWER:
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
            
            # フォロワーファイルパスフォーマットの決定
            followxx_file_path_format = const_util.FOLLOWER_FILE_PATH
        
        # フォロイー(フォロワー)ページの件数が0件の場合
        if len(followxx_pages) == 0:
            pyl.log_inf(lg, f'フォロイー(フォロワー)ページの件数が0件です。(user_id:{user_id})')
        else:
            # フォロイー(フォロワー)データフレームの初期化
            followxx_df: pd.DataFrame = pd.DataFrame(columns=const_util.LIST_MEMBER_HEADER)
            
            # フォロイー(フォロワー)データフレームへの格納
            for followxxs_by_page in followxx_pages:
                # followxx: tweepy.models.User
                for followxx in followxxs_by_page:
                    # ユーザ情報データフレームの格納
                    user_info_df = pd.DataFrame(
                            [[
                                followxx.screen_name,
                                followxx.name,
                                const_util.ACCOUNT_URL.format(followxx.screen_name)
                            ]],
                            columns=const_util.LIST_MEMBER_HEADER
                        )
                    followxx_df = pd.concat([followxx_df, user_info_df], ignore_index=True)
            
            # フォロイー(フォロワー)ファイルパスの生成
            user_info: Any = twitter_users_util.get_user_info(api, user_id)
            followxx_file_path: str = \
                followxx_file_path_format.format(user_info.screen_name, user_info.name)
            
            # フォロイー(フォロワー)データフレームの保存
            pyl.log_inf(lg, f'フォロイー(フォロワー)(追加分先頭n行)：\n{followxx_df.head(5)}')
            pyl.log_inf(lg, f'フォロイー(フォロワー)(追加分末尾n行)：\n{followxx_df.tail(5)}')
            pandas_util.save_list_member_df(followxx_df, followxx_file_path)
        
        # レート制限の表示
        if enum_of_item_proc_target == EnumOfItemProcTarget.FOLLOWEE:
            twitter_developer_util.show_rate_limit_of_friends_list(api)
        elif enum_of_item_proc_target == EnumOfItemProcTarget.FOLLOWER:
            twitter_developer_util.show_rate_limit_of_followers_list(api)
        
        pyl.log_inf(lg, f'Twitterフォロイー(フォロワー)エクスポートを終了します。')
    except Exception as e:
        raise(e)
    
    return None

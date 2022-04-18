from logging import Logger
from typing import Optional

import pandas as pd
import python_lib_for_me as pyl
import tweepy

from twitter_app.util import const_util, pandas_util
from twitter_app.util.twitter_api_v1_1.standard import twitter_developer_util, twitter_users_util


def do_logic(
        api: tweepy.API,
        list_df: pd.DataFrame
    ) -> None:
    
    '''
    ロジック実行
    
    Args:
        api (tweepy.API)       : API
        list_df (pd.DataFrame) : リストデータフレーム
    
    Returns:
        -
    '''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'Twitterリストエクスポートを開始します。')
        
        # Pandasオプション設定
        pd.set_option('display.unicode.east_asian_width', True)
        
        # レート制限の表示
        twitter_developer_util.show_rate_limit_of_lists_members(api)
        
        # リストのエクスポート
        for _, list_ in list_df.iterrows():
            # リストメンバーページの取得
            list_member_pages = twitter_users_util.get_list_member_pages(
                    api,
                    str(list_[const_util.LIST_HEADER[1]])
                )
            
            # リストメンバーデータフレームの初期化
            list_member_df: pd.DataFrame = pd.DataFrame(columns=const_util.LIST_MEMBER_HEADER)
            
            # リストメンバーデータフレームへの格納
            for list_members_by_page in list_member_pages:
                # list_member: tweepy.models.User
                for list_member in list_members_by_page:
                    # ユーザ情報データフレームの格納
                    user_info_df = pd.DataFrame(
                            [[
                                list_member.screen_name,
                                list_member.name,
                                const_util.ACCOUNT_URL.format(list_member.screen_name)
                            ]],
                            columns=const_util.LIST_MEMBER_HEADER
                        )
                    list_member_df = pd.concat([list_member_df, user_info_df], ignore_index=True)
            
            # リストメンバーファイルパスの生成
            list_member_file_path = const_util.LIST_MEMBER_FILE_PATH.format(
                str(list_[const_util.LIST_HEADER[2]]))
            
            # リストメンバーデータフレームの保存
            pyl.log_inf(lg, f'リストメンバー(追加分先頭n行)：\n{list_member_df.head(5)}')
            pyl.log_inf(lg, f'リストメンバー(追加分末尾n行)：\n{list_member_df.tail(5)}')
            pandas_util.save_list_member_df(list_member_df, list_member_file_path)
        
        # レート制限の表示
        twitter_developer_util.show_rate_limit_of_lists_members(api)
    except Exception as e:
        raise(e)
    finally:
        pyl.log_inf(lg, f'Twitterリストエクスポートを終了します。')
    
    return None

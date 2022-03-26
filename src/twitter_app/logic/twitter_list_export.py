from enum import IntEnum, auto
from logging import Logger
from typing import Optional

import pandas as pd
import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet

from twitter_app.util import const_util, pandas_util
from twitter_app.util.twitter_api_v1_1.standard import twitter_developer_util, twitter_users_util


class EnumOfListProcTarget(IntEnum):
    ALL = auto()
    ID = auto()
    NAME = auto()


def do_logic_that_show_list(
        api: tweepy.API,
        enum_of_list_proc_target: EnumOfListProcTarget,
        list_id_or_name_of_csv_format: str
    ) -> pd.DataFrame:
    
    '''
    ロジック実行
    
    Args:
        api (tweepy.API)                                : API
        enum_of_list_proc_target (EnumOfListProcTarget) : リスト処理対象
        list_id_or_name_of_csv_format (str)             : リストID(名前)(csv形式)
    
    Returns:
        pd.DataFrame: リストデータフレーム
    '''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'Twitterリスト表示を開始します。')
        
        # Pandasオプション設定
        pd.set_option('display.unicode.east_asian_width', True)
        
        # リスト(複数)の取得
        lists: ResultSet = twitter_users_util.get_lists(api)
        
        # リストデータフレームの初期化
        list_df: pd.DataFrame = pd.DataFrame(columns=const_util.LIST_HEADER)
        
        # リストデータフレームへの格納
        for list_ in lists:
            # リスト情報の取得
            creation_datetime: str = pyl.convert_timestamp_to_jst(str(list_.created_at))
            list_id: str = list_.id
            num_of_members: int = list_.member_count
            list_name: str = list_.name
            
            # リスト情報の格納(リスト処理対象ごと)
            list_info_df: pd.DataFrame
            if enum_of_list_proc_target == EnumOfListProcTarget.ALL:
                list_info_df = pd.DataFrame(
                    [[creation_datetime, list_id, list_name, num_of_members]],
                    columns=const_util.LIST_HEADER)
                list_df = pd.concat([list_df, list_info_df], ignore_index=True)
            elif enum_of_list_proc_target == EnumOfListProcTarget.ID:
                # リストIDリスト(引数のCSVから)の生成
                list_ids: list[str] = \
                    pyl.generate_str_list_from_csv(list_id_or_name_of_csv_format)
                
                # リストID(APIから)がリストIDリスト(引数のCSVから)に含まれている場合
                if list_id in list_ids:
                    list_info_df = pd.DataFrame(
                        [[creation_datetime, list_id, list_name, num_of_members]],
                        columns=const_util.LIST_HEADER)
                    list_df = pd.concat([list_df, list_info_df], ignore_index=True)
            elif enum_of_list_proc_target == EnumOfListProcTarget.NAME:
                # リスト名リスト(引数のCSVから)の生成
                list_names: list[str] = \
                    pyl.generate_str_list_from_csv(list_id_or_name_of_csv_format)
                
                # リスト名(APIから)がリスト名リスト(引数のCSVから)に含まれている場合
                match_with_list_names: bool = False
                for name in list_names:
                    if name in list_name:
                        match_with_list_names = True
                
                # リスト名一致有無がTrueの場合
                if match_with_list_names == True:
                    list_info_df = pd.DataFrame(
                        [[creation_datetime, list_id, list_name, num_of_members]],
                        columns=const_util.LIST_HEADER)
                    list_df = pd.concat([list_df, list_info_df], ignore_index=True)
        
        # リストデータフレームの表示
        pyl.log_inf(lg, f'リスト：\n{list_df}')
        
        pyl.log_inf(lg, f'Twitterリスト表示を終了します。')
    except Exception as e:
        raise(e)
    
    return list_df


def do_logic_that_export_list(
        api: tweepy.API,
        enum_of_list_proc_target: EnumOfListProcTarget,
        list_id_or_name_of_csv_format: str
    ) -> None:
    
    '''
    ロジック実行
    
    Args:
        api (tweepy.API)                                : API
        enum_of_list_proc_target (EnumOfListProcTarget) : リスト処理対象
        list_id_or_name_of_csv_format (str)             : リストID(名前)(csv形式)
    
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
        
        # ロジック(Twitterリスト表示)の実行
        list_df: pd.DataFrame = do_logic_that_show_list(
            api, enum_of_list_proc_target, list_id_or_name_of_csv_format)
        
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
        
        pyl.log_inf(lg, f'Twitterリストエクスポートを終了します。')
    except Exception as e:
        raise(e)
    
    return None

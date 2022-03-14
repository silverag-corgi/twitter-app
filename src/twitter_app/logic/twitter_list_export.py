from datetime import datetime
from enum import IntEnum, auto
from logging import Logger
from typing import Optional

import pandas as pd
import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet

from twitter_app.util import const_util, pandas_util
from twitter_app.util.twitter_api_standard_v1_1 import twitter_developer_util, twitter_users_util


class TWITTER_LIST_PROC_TARGET(IntEnum):
    ALL = auto()
    ID = auto()
    NAME = auto()


def do_logic_that_show_twitter_list(
        api: tweepy.API,
        kind_of_proc_targets: TWITTER_LIST_PROC_TARGET,
        csv_of_twitter_list_idname: str
    ) -> pd.DataFrame:
    
    '''
    ロジック実行
    
    Args:
        api (tweepy.API)                                : API
        kind_of_proc_targets (TWITTER_LIST_PROC_TARGET) : Twitterリスト処理対象の種類
        csv_of_twitter_list_idname (str)                : TwitterリストID(名前)のCSV
    
    Returns:
        pd.DataFrame: Twitterリスト一覧データフレーム
    '''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'Twitterリスト表示を開始します。')
        
        # Pandasオプション設定
        pd.set_option('display.unicode.east_asian_width', True)
        
        # Twitterリスト一覧の取得
        twitter_lists: ResultSet = twitter_users_util.get_twitter_lists(api)
        
        # Twitterリスト一覧データフレームの初期化
        twitter_lists_df: pd.DataFrame = pd.DataFrame(columns=const_util.TWITTER_LISTS_HEADER)
        
        # Twitterリスト一覧データフレームへの格納
        for twitter_list in twitter_lists:
            # Twitterリスト情報の取得
            creation_datetime_src: datetime = twitter_list.created_at
            creation_timestamp_src: str = creation_datetime_src.strftime('%Y-%m-%d %H:%M:%S%z')
            creation_timestamp: str = pyl.convert_timestamp_to_jst(creation_timestamp_src)
            twitter_list_id: str = twitter_list.id
            num_of_members: int = twitter_list.member_count
            twitter_list_name: str = twitter_list.name
            
            # Twitterリスト情報の格納(処理対象の種類ごと)
            twitter_list_info_df: pd.DataFrame
            if kind_of_proc_targets == TWITTER_LIST_PROC_TARGET.ALL:
                twitter_list_info_df = pd.DataFrame(
                    [[creation_timestamp, twitter_list_id, twitter_list_name, num_of_members]],
                    columns=const_util.TWITTER_LISTS_HEADER)
                twitter_lists_df = pd.concat(
                    [twitter_lists_df, twitter_list_info_df], ignore_index=True)
            elif kind_of_proc_targets == TWITTER_LIST_PROC_TARGET.ID:
                # TwitterリストIDリスト(引数のCSVから)の生成
                twitter_list_ids: list[str] = \
                    pyl.generate_str_list_from_csv(csv_of_twitter_list_idname)
                
                # TwitterリストID(APIから)がTwitterリストIDリスト(引数のCSVから)に含まれている場合
                if twitter_list_id in twitter_list_ids:
                    twitter_list_info_df = pd.DataFrame(
                        [[creation_timestamp, twitter_list_id, twitter_list_name, num_of_members]],
                        columns=const_util.TWITTER_LISTS_HEADER)
                    twitter_lists_df = pd.concat(
                        [twitter_lists_df, twitter_list_info_df], ignore_index=True)
            elif kind_of_proc_targets == TWITTER_LIST_PROC_TARGET.NAME:
                # TwitterリストIDリスト(引数のCSVから)の生成
                twitter_list_names: list[str] = \
                    pyl.generate_str_list_from_csv(csv_of_twitter_list_idname)
                
                # Twitterリスト名(APIから)がTwitterリスト名リスト(引数のCSVから)に含まれている場合
                match_with_twitter_list_names: bool = False
                for name in twitter_list_names:
                    if name in twitter_list_name:
                        match_with_twitter_list_names = True
                
                # Twitterリスト名一致有無がTrueの場合
                if match_with_twitter_list_names == True:
                    twitter_list_info_df = pd.DataFrame(
                        [[creation_timestamp, twitter_list_id, twitter_list_name, num_of_members]],
                        columns=const_util.TWITTER_LISTS_HEADER)
                    twitter_lists_df = pd.concat(
                        [twitter_lists_df, twitter_list_info_df], ignore_index=True)
        
        # Twitterリスト一覧データフレームの表示
        pyl.log_inf(lg, f'Twitterリスト一覧：\n{twitter_lists_df}')
        
        pyl.log_inf(lg, f'Twitterリスト表示を終了します。')
    except Exception as e:
        raise(e)
    
    return twitter_lists_df


def do_logic_that_export_twitter_list(
        api: tweepy.API,
        kind_of_proc_targets: TWITTER_LIST_PROC_TARGET,
        csv_of_twitter_list_idname: str
    ) -> None:
    
    '''
    ロジック実行
    
    Args:
        api (tweepy.API)                                : API
        kind_of_proc_targets (TWITTER_LIST_PROC_TARGET) : Twitterリスト処理対象の種類
        csv_of_twitter_list_idname (str)                : TwitterリストID(名前)のCSV
    
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
        twitter_lists_df: pd.DataFrame = do_logic_that_show_twitter_list(
            api, kind_of_proc_targets, csv_of_twitter_list_idname)
        
        # レート制限の表示
        twitter_developer_util.show_rate_limit_of_lists_members(api)
        
        # Twitterリストのエクスポート
        for _, twitter_list_row in twitter_lists_df.iterrows():
            # Twitterリストメンバーページの取得
            twitter_list_member_pages = twitter_users_util.get_twitter_list_member_pages(
                    api,
                    str(twitter_list_row[const_util.TWITTER_LISTS_HEADER[1]])
                )
            
            # Twitterリストデータフレームの初期化
            twitter_list_df: pd.DataFrame = \
                pd.DataFrame(columns=const_util.TWITTER_LIST_FILE_HEADER)
            
            # Twitterリストデータフレームへの格納
            for twitter_list_members_by_page in twitter_list_member_pages:
                # twitter_list_member: tweepy.models.User
                for twitter_list_member in twitter_list_members_by_page:
                    # Twitterリスト情報の格納
                    twitter_list_info_df = pd.DataFrame(
                        [[twitter_list_member.screen_name, twitter_list_member.name]],
                        columns=const_util.TWITTER_LIST_FILE_HEADER)
                    twitter_list_df = pd.concat(
                        [twitter_list_df, twitter_list_info_df], ignore_index=True)
                    pyl.log_inf(lg, f'ユーザID：{twitter_list_member.screen_name: <15}' +
                                    f'ユーザ名：{twitter_list_member.name}')
            
            # Twitterリストファイルパスの生成
            twitter_list_path = const_util.TWITTER_LIST_FILE_PATH.format(
                str(twitter_list_row[const_util.TWITTER_LISTS_HEADER[2]]))
            
            # Twitterリストデータフレームの保存
            pyl.log_inf(lg, f'Twitterリスト(追加分先頭n行)：\n{twitter_list_df.head(5)}')
            pyl.log_inf(lg, f'Twitterリスト(追加分末尾n行)：\n{twitter_list_df.tail(5)}')
            pandas_util.save_twitter_list_df(twitter_list_df, twitter_list_path)
        
        # レート制限の表示
        twitter_developer_util.show_rate_limit_of_lists_members(api)
        
        pyl.log_inf(lg, f'Twitterリストエクスポートを終了します。')
    except Exception as e:
        raise(e)
    
    return None

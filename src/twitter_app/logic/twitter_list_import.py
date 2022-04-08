import glob
import os
from logging import Logger
from typing import Any, Optional

import pandas as pd
import python_lib_for_me as pyl
import tweepy

from twitter_app.util import const_util, pandas_util
from twitter_app.util.twitter_api_v1_1.standard import twitter_users_util


def do_logic(
        api: tweepy.API,
        list_member_file_path_with_wildcard: str,
        header_line_num: int
    ) -> None:
    
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    list_: Any = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'Twitterリストインポートを開始します。')
        
        # リストメンバーファイルパスの取得
        list_member_file_paths: list[str] = glob.glob(list_member_file_path_with_wildcard)
        
        # リストメンバーファイルの件数が0件の場合
        if len(list_member_file_paths) == 0:
            pyl.log_inf(lg, f'リストメンバーファイルの件数が0件です。' +
                            f'(list_member_file_path:{list_member_file_path_with_wildcard})')
        else:
            # TwitterAPIの実行
            for list_member_file_path in list_member_file_paths:
                # リスト名の生成
                list_name: str = os.path.splitext(os.path.basename(list_member_file_path))[0]
                
                # リストの破棄
                twitter_users_util.destroy_list(api, list_name)
                
                # リストの生成
                list_ = twitter_users_util.generate_list(api, list_name)
                
                # リストメンバーデータフレームの取得(リストメンバーファイルの読み込み)
                list_member_df: pd.DataFrame = \
                    pandas_util.read_list_member_file(list_member_file_path, header_line_num)
                
                # ユーザの追加
                twitter_users_util.add_users_to_list(
                        api,
                        list_.id,
                        [str(list_member[const_util.LIST_MEMBER_HEADER[0]]).strip()
                            for _, list_member in list_member_df.iterrows()],
                        [str(list_member[const_util.LIST_MEMBER_HEADER[1]])
                            for _, list_member in list_member_df.iterrows()]
                    )
        
        pyl.log_inf(lg, f'Twitterリストインポートを終了します。')
    except Exception as e:
        # リストの破棄
        if list_ is not None:
            twitter_users_util.destroy_list(api, list_.name)
        
        raise(e)
    
    return None

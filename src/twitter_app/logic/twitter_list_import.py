import glob
import os
from logging import Logger
from typing import Optional

import pandas as pd
import python_lib_for_me as pyl
import tweepy

from twitter_app.util import const_util, pandas_util
from twitter_app.util.twitter_api_standard_v1_1 import twitter_users_util


def do_logic(
        api: tweepy.API,
        twitter_list_csv_file_path_with_wildcard: str,
        header_line_num: int
    ) -> None:
    
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    twitter_list: Optional[tweepy.List] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'Twitterリストインポートを開始します。')
        
        # TwitterリストCSVファイルパスの取得
        twitter_list_csv_file_paths: list[str] = glob.glob(twitter_list_csv_file_path_with_wildcard)
        
        # TwitterリストCSVファイルの件数が0件の場合
        if len(twitter_list_csv_file_paths) == 0:
            pyl.log_inf(lg, f'TwitterリストCSVファイルの件数が0件です。' +
                            f'(twitter_list_csv_file_path:' +
                            f'{twitter_list_csv_file_path_with_wildcard})')
        else:
            # TwitterAPIの実行
            for twitter_list_csv_file_path in twitter_list_csv_file_paths:
                # Twitterリスト名の生成
                twitter_list_name: str = \
                    os.path.splitext(os.path.basename(twitter_list_csv_file_path))[0]
                
                # Twitterリストが存在する場合
                if twitter_users_util.has_twitter_list(api, twitter_list_name) == True:
                    twitter_users_util.destroy_twitter_list(api, twitter_list_name)
                
                # Twitterリストの生成
                twitter_list = twitter_users_util.generate_twitter_list(api, twitter_list_name)
                
                # Twitterリストデータフレームの取得(TwitterリストCSVファイルの読み込み)
                twitter_list_df: pd.DataFrame = \
                    pandas_util.read_twitter_list_file(twitter_list_csv_file_path)
                
                # ユーザの追加
                pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
                for _, twitter_list_row in twitter_list_df.iterrows():
                    if len(twitter_list_row) >= 2:
                        twitter_users_util.add_user_to_twitter_list(
                                api,
                                twitter_list,
                                str(twitter_list_row[const_util.TWITTER_LIST_FILE_HEADER[0]]),
                                str(twitter_list_row[const_util.TWITTER_LIST_FILE_HEADER[1]])
                            )
                
                # Twitterリストの破棄(ユーザが0人の場合)
                if len(twitter_list_df) == 0:
                    twitter_users_util.destroy_twitter_list(api, twitter_list_name)
        
        pyl.log_inf(lg, f'Twitterリストインポートを終了します。')
    except Exception as e:
        # Twitterリストの破棄
        if twitter_list is not None:
            twitter_users_util.destroy_twitter_list(api, twitter_list.name)
        
        raise(e)
    
    return None

import csv
import glob
import os
from logging import Logger
from typing import Any, Optional, TextIO

import python_lib_for_me as pyl
import tweepy

from twitter_lib_for_me.util.twitter_api_standard_v1_1 import twitter_users_util


def do_logic(api: tweepy.API, twitter_list_file_path_with_wildcard: str) -> None:
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    twitter_list: Optional[tweepy.List] = None
    
    try:
        # ロガー取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'Twitterリスト生成を開始します。')
        
        # Twitterリストファイルパスの取得
        twitter_list_file_paths: list[str] = glob.glob(twitter_list_file_path_with_wildcard)
        
        # Twitterリストファイルの件数が0件の場合
        if len(twitter_list_file_paths) == 0:
            pyl.log_inf(lg, f'Twitterリストファイルの件数が0件です。' +
                            f'(twitter_list_file_path:{twitter_list_file_path_with_wildcard})')
        else:
            # TwitterAPIの実行
            for twitter_list_file_path in twitter_list_file_paths:
                # Twitterリストが存在しない場合
                twitter_list_name: str = \
                    os.path.splitext(os.path.basename(twitter_list_file_path))[0]
                if twitter_users_util.has_twitter_list(api, twitter_list_name) == False:
                    # Twitterリストの生成
                    twitter_list = twitter_users_util.generate_twitter_list(api, twitter_list_name)
                    
                    # Twitterリストファイルの読み込み
                    twitter_list_file_object: TextIO = open(
                            twitter_list_file_path,
                            encoding='utf_8',
                            newline='\r\n'
                        )
                    twitter_list_file_lines: Any = csv.reader(
                            twitter_list_file_object,
                            delimiter=',',
                            doublequote=True,
                            lineterminator='\r\n',
                            quotechar='"',
                            skipinitialspace=False
                        )
                    
                    # ユーザの追加
                    pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
                    for twitter_list_file_line in twitter_list_file_lines:
                        if len(twitter_list_file_line) >= 2:
                            twitter_users_util.add_user(
                                    api,
                                    twitter_list,
                                    twitter_list_file_line[0],
                                    twitter_list_file_line[1]
                                )
                    
                    # Twitterリストの破棄(ユーザが0人の場合)
                    if twitter_list_file_lines.line_num == 0:
                        twitter_users_util.destroy_twitter_list(api, twitter_list)
        
        pyl.log_inf(lg, f'Twitterリスト生成を終了します。')
    except Exception as e:
        # Twitterリストの破棄
        if twitter_list is not None:
            twitter_users_util.destroy_twitter_list(api, twitter_list)
        
        raise(e)
    
    return None

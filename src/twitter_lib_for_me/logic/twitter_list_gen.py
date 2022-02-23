import csv
import glob
import io
import os
from logging import Logger
from typing import Iterator, Optional

import python_lib_for_me as mylib
import tweepy
from twitter_lib_for_me.util.twitter_api_standard_v1_1 import \
    twitter_tweets_util


def do_logic(api: tweepy.API, twitter_list_file_path_with_wildcard: str) -> None:
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    twitter_list: Optional[tweepy.List] = None
    
    try:
        # ロガー取得
        lg = mylib.get_logger(__name__)
        lg.info(f'Twitterリスト生成を開始します。')
        
        # Twitterリストファイルパスの取得
        twitter_list_file_paths: list[str] = glob.glob(twitter_list_file_path_with_wildcard)
        
        # 実行要否の判定
        should_execute: bool = True
        if len(twitter_list_file_paths) == 0:
            should_execute = False
            lg.info(f'Twitterリストファイルの件数が0件です。' +
                    f'(twitter_list_file_path:{twitter_list_file_path_with_wildcard})')
        
        if should_execute == True:
            # TwitterAPIの実行
            for twitter_list_file_path in twitter_list_file_paths:
                # Twitterリスト生成要否の判定
                should_generate: bool = True
                twitter_list_name: str = \
                    os.path.splitext(os.path.basename(twitter_list_file_path))[0]
                if twitter_tweets_util.has_twitter_list(api, twitter_list_name) == True:
                    should_generate = False
                
                if should_generate == True:
                    # Twitterリストの生成
                    twitter_list = twitter_tweets_util.generate_twitter_list(api, twitter_list_name)
                    
                    # Twitterリストファイルの読み込み
                    twitter_list_file_object: io.TextIOWrapper = open(
                            twitter_list_file_path,
                            encoding='utf_8',
                            newline='\r\n'
                        )
                    twitter_list_file_lines: Iterator = csv.reader(
                            twitter_list_file_object,
                            delimiter=',',
                            doublequote=True,
                            lineterminator='\r\n',
                            quotechar='"',
                            skipinitialspace=False
                        )
                    
                    # ユーザの追加
                    lg.info(f'時間がかかるため気長にお待ちください。')
                    for twitter_list_file_line in twitter_list_file_lines:
                        if len(twitter_list_file_line) >= 2:
                            twitter_tweets_util.add_user(
                                    api,
                                    twitter_list,
                                    twitter_list_file_line[0],
                                    twitter_list_file_line[1]
                                )
                    
                    # Twitterリストの破棄(ユーザが0人の場合)
                    if twitter_list_file_lines.line_num == 0:
                        twitter_tweets_util.destroy_twitter_list(api, twitter_list)
        
        lg.info(f'Twitterリスト生成を終了します。')
    except Exception as e:
        # Twitterリストの破棄
        if twitter_list is not None:
            twitter_tweets_util.destroy_twitter_list(api, twitter_list)
        
        raise(e)
    
    return None

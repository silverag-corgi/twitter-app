import csv
import glob
import io
import os
from logging import Logger

import python_lib_for_me
import tweepy
from twitter_lib_for_me.util import twitter_list_util


def do_logic(api: tweepy.API, csv_file_path_with_regex: str) -> None:
    '''ロジック実行'''

    try:
        # ロガー取得
        lg: Logger = python_lib_for_me.get_logger(__name__)

        # CSVファイル存在確認
        csv_file_paths: list[str] = glob.glob(csv_file_path_with_regex)
        if __has_csv_files(csv_file_paths) == False:
            return None
        
        # TwitterAPI実行
        for csv_file_path in csv_file_paths:
            # Twitterリスト存在確認
            csv_file_name: str = os.path.splitext(os.path.basename(csv_file_path))[0]
            if twitter_list_util.has_twitter_list(api, csv_file_name) == True:
                return None

            # Twitterリスト作成
            twitter_list: tweepy.List = twitter_list_util.generate_twitter_list(api, csv_file_name)

            # CSVファイル読み込み
            csv_file_obj: io.TextIOWrapper = open(csv_file_path, 'r', encoding='utf_8', newline='\r\n')
            csv_file_rdr: csv.reader = csv.reader(
                csv_file_obj, delimiter=',', doublequote=True,
                lineterminator='\r\n', quotechar='"', skipinitialspace=False)

            # ユーザ追加
            for row_list in csv_file_rdr:
                if len(row_list) != 0 and len(row_list) == 2:
                    twitter_list_util.add_user(api, twitter_list, row_list[0], row_list[1])
    except Exception as e:
        # Twitterリスト削除
        if twitter_list is not None:
           api.destroy_list(list_id=twitter_list.id)
           if lg is not None:
               lg.info(f'例外発生により、Twitterリストを削除しました。(リスト名：{twitter_list.name})')

        raise(e)

    return None


def __has_csv_files(csv_file_paths: list[str]) -> bool:
    '''CSVファイル存在確認'''

    try:
        lg: Logger = python_lib_for_me.get_logger(__name__)

        if len(csv_file_paths) == 0:
            lg.info(f'CSVファイルの件数が0件です。')
            return False
    except Exception as e:
        raise(e)

    return True

import csv
import glob
import os

import tweepy


def do_logic(api: tweepy.API, csv_file_path: str) -> None:
    '''ロジック実行'''

    try:
        # CSVファイル存在確認
        csv_file_paths = glob.glob(csv_file_path)
        if __has_csv_files(csv_file_paths) == False:
            return None
        
        # TwitterAPI実行
        for csv_file_path in csv_file_paths:
            # Twitterリスト存在確認
            csv_file_name = os.path.splitext(os.path.basename(csv_file_path))[0]
            if __has_twitter_list(api, csv_file_name) == True:
                return None

            # Twitterリスト作成
            twitter_list = __generate_twitter_list(api, csv_file_name)

            # CSVファイル読み込み
            csv_file_obj = open(csv_file_path, 'r', encoding='utf_8', newline='\r\n')
            csv_file_rdr = csv.reader(csv_file_obj, delimiter=',', doublequote=True, lineterminator='\r\n', quotechar='"', skipinitialspace=False)

            # ユーザ追加
            for row in csv_file_rdr:
                if len(row) != 0 and len(row) == 2:
                    __add_user(api, twitter_list, row[0], row[1])
    except Exception as e:
        # Twitterリスト削除
        if twitter_list is not None:
           api.destroy_list(list_id=twitter_list.id)
           print(f'例外発生により、Twitterリストを削除しました。(リスト名：{twitter_list.name})')

        raise(e)

    return None


def __has_csv_files(csv_file_paths: str) -> bool:
    '''CSVファイル存在確認'''

    if len(csv_file_paths) == 0:
        print(f'CSVファイルの件数が0件です。')
        return False

    return True


def __has_twitter_list(api: tweepy.API, list_name: str) -> bool:
    '''Twitterリスト存在確認'''

    twitter_lists = api.get_lists()
    for twitter_list in twitter_lists:
        if twitter_list.name == list_name:
            print(f'Twitterリストが既に存在します。(リスト名：{twitter_list.name})')
            return True

    return False


def __generate_twitter_list(api: tweepy.API, twitter_list_name: str) -> tweepy.List:
    '''Twitterリスト作成'''

    try:
        twitter_list = api.create_list(twitter_list_name, mode='private', description='')
        print(f'Twitterリスト作成に成功しました。(リスト名：{twitter_list.name})')
    except Exception as e:
        print(f'Twitterリスト作成に失敗しました。')
        raise(e)

    return twitter_list


def __add_user(api: tweepy.API, twitter_list: tweepy.List, user_id: str, user_name: str) -> None:
    '''ユーザ追加'''

    try:
        api.add_list_member(list_id=twitter_list.id, screen_name=user_id)
        print(f'ユーザ追加に成功しました。(ユーザID：{user_id}、ユーザ名：{user_name})')
    except Exception as e:
        # ユーザが鍵付きや削除済みなどの場合
        print(f'ユーザ追加に失敗しました。(ユーザID：{user_id}、ユーザ名：{user_name})')

    return None

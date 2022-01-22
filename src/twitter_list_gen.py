import csv
import glob
import os

import tweepy


def main(api: tweepy.API) -> None:
    '''メイン'''

    try:
        # 入力フォルダ読み込み
        input_file_paths = glob.glob('input/*.csv')
        for input_file_path in input_file_paths:
            # Twitterリスト(入力ファイル名)存在確認
            input_file_name = os.path.splitext(os.path.basename(input_file_path))[0]
            has_twitter_list = __has_twitter_list(api, input_file_name)
            if has_twitter_list == False:
                # Twitterリスト作成
                twitter_list = __generate_twitter_list(api, input_file_name)

                # 入力ファイル読み込み
                input_file_obj = open(input_file_path, 'r', encoding='utf_8', newline='\r\n')
                input_file_path = csv.reader(input_file_obj, delimiter=',', doublequote=True, lineterminator='\r\n', quotechar='"', skipinitialspace=False)

                # ユーザ追加
                for input_row in input_file_path:
                    __add_user(api, twitter_list, input_row[0], input_row[1])
    except Exception as e:
        raise(e)

    return None


def __has_twitter_list(api: tweepy.API, list_name: str) -> bool:
    '''Twitterリスト存在確認'''

    twitter_lists = api.get_lists()
    for twitter_list in twitter_lists:
        if twitter_list.name == list_name:
            print(f'リストが既に存在します。(リスト名：{twitter_list.name})')
            return True

    return False


def __generate_twitter_list(api: tweepy.API, twitter_list_name: str) -> tweepy.List:
    '''Twitterリスト作成'''

    try:
        twitter_list = api.create_list(twitter_list_name, mode='private', description='')
        print(f'リスト作成に成功しました。(リスト名：{twitter_list.name})')
    except Exception as e:
        print(f'リスト作成に失敗しました。')
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

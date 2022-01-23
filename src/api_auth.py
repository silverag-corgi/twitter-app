import io
import json
from typing import Any, Dict

import tweepy


def do_logic() -> tweepy.API:
    '''ロジック実行'''

    try:
        json_data: Dict[Any, Any] = __get_api_auth_info_json()
        api: tweepy.API = __exec_twitter_auth(json_data)
    except Exception as e:
        raise(e)

    return api


def __get_api_auth_info_json() -> Dict[Any, Any]:
    '''API認証情報JSON取得'''

    try:
        json_file_obj: io.TextIOWrapper = open('config/api_auth_info.json', 'r')
        json_data_dct: Dict[Any, Any] = json.load(json_file_obj)

        print(f'API認証情報JSON取得に成功しました。')
    except Exception as e:
        print(f'API認証情報JSON取得に失敗しました。')
        raise(e)

    return json_data_dct


def __exec_twitter_auth(json_data_dct: Dict[Any, Any]) -> tweepy.API:
    '''Twitter認証実行'''

    try:
        consumer_key: str = json_data_dct['twitter_auth']['consumer_key']
        consumer_secret: str = json_data_dct['twitter_auth']['consumer_secret']
        access_token: str = json_data_dct['twitter_auth']['access_token']
        access_token_secret: str = json_data_dct['twitter_auth']['access_token_secret']

        auth: tweepy.OAuthHandler = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api: tweepy.API = tweepy.API(auth)
        api.verify_credentials()

        print(f'Twitter認証実行に成功しました。')
    except Exception as e:
        print(f'Twitter認証実行に失敗しました。')
        raise(e)

    return api

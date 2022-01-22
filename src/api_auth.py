import json
from typing import Any, Dict

import tweepy


def main() -> tweepy.API:
    '''メイン'''

    try:
        json_data = __get_api_auth_info_json()
        api = __exec_twitter_auth(json_data)
    except Exception as e:
        raise(e)

    return api


def __get_api_auth_info_json() -> Dict[Any, Any]:
    '''API認証情報JSON取得'''

    try:
        json_file = open('config/api_auth_info.json', 'r')
        json_data = json.load(json_file)

        print(f'API認証情報JSON取得に成功しました。')
    except Exception as e:
        print(f'API認証情報JSON取得に失敗しました。')
        raise(e)

    return json_data


def __exec_twitter_auth(json_data: Dict[Any, Any]) -> tweepy.API:
    '''Twitter認証実行'''

    try:
        consumer_key = json_data['twitter_auth']['consumer_key']
        consumer_secret = json_data['twitter_auth']['consumer_secret']
        access_token = json_data['twitter_auth']['access_token']
        access_token_secret = json_data['twitter_auth']['access_token_secret']

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)
        api.verify_credentials()

        print(f'Twitter認証実行に成功しました。')
    except Exception as e:
        print(f'Twitter認証実行に失敗しました。')
        raise(e)

    return api

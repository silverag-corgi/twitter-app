import io
import json
from logging import Logger
from typing import Any, Optional

import python_lib_for_me as mylib
import tweepy


def do_logic() -> tweepy.API:
    '''ロジック実行'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = mylib.get_logger(__name__)
        lg.info(f'API認証を開始します。')
        
        json_data: dict[Any, Any] = __get_api_auth_info_json()
        api: tweepy.API = __authorize_twitter(json_data)
        
        lg.info(f'API認証を終了します。')
    except Exception as e:
        raise(e)
        
    return api


def __get_api_auth_info_json() -> dict[Any, Any]:
    '''API認証情報JSON取得'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = mylib.get_logger(__name__)
        
        json_file_obj: io.TextIOWrapper = open('config/api_auth_info.json', 'r')
        json_data_dct: dict[Any, Any] = json.load(json_file_obj)
        
        lg.info(f'API認証情報JSON取得に成功しました。')
    except Exception as e:
        if lg is not None:
            lg.info(f'API認証情報JSON取得に失敗しました。')
        raise(e)
    
    return json_data_dct


def __authorize_twitter(json_data_dct: dict[Any, Any]) -> tweepy.API:
    '''Twitter認証'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = mylib.get_logger(__name__)
        
        consumer_key:        str = json_data_dct['twitter_auth']['consumer_key']
        consumer_secret:     str = json_data_dct['twitter_auth']['consumer_secret']
        access_token:        str = json_data_dct['twitter_auth']['access_token']
        access_token_secret: str = json_data_dct['twitter_auth']['access_token_secret']
        
        auth: tweepy.OAuthHandler = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        api: tweepy.API = tweepy.API(auth, wait_on_rate_limit=True)
        api.verify_credentials()
        
        lg.info(f'Twitter認証に成功しました。')
    except Exception as e:
        if lg is not None:
            lg.info(f'Twitter認証に失敗しました。')
        raise(e)
    
    return api

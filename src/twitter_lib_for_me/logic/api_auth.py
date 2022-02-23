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
        
        api_auth_infos: dict[Any, Any] = __get_api_auth_infos()
        api: tweepy.API = __authorize_twitter(api_auth_infos)
        
        lg.info(f'API認証を終了します。')
    except Exception as e:
        raise(e)
        
    return api


def __get_api_auth_infos() -> dict[Any, Any]:
    '''API認証情報取得'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = mylib.get_logger(__name__)
        
        api_auth_info_file: io.TextIOWrapper = open('config/api_auth_info.json', 'r')
        api_auth_infos: dict[Any, Any] = json.load(api_auth_info_file)
        
        lg.info(f'API認証情報取得に成功しました。')
    except Exception as e:
        if lg is not None:
            lg.info(f'API認証情報取得に失敗しました。')
        raise(e)
    
    return api_auth_infos


def __authorize_twitter(api_auth_infos: dict[Any, Any]) -> tweepy.API:
    '''Twitter認証'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = mylib.get_logger(__name__)
        
        consumer_key:        str = api_auth_infos['twitter_auth_info']['consumer_key']
        consumer_secret:     str = api_auth_infos['twitter_auth_info']['consumer_secret']
        access_token:        str = api_auth_infos['twitter_auth_info']['access_token']
        access_token_secret: str = api_auth_infos['twitter_auth_info']['access_token_secret']
        
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

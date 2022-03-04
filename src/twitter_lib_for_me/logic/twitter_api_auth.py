import json
from logging import Logger
from typing import Any, Optional, TextIO

import python_lib_for_me as pyl
import tweepy


def do_logic_of_api() -> tweepy.API:
    '''ロジック実行(API)'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'TwitterAPI認証(API)を開始します。')
        
        twitter_api_auth_info: dict[Any, Any] = __get_twitter_api_auth_info()
        api: tweepy.API = __generate_api(twitter_api_auth_info)
        
        pyl.log_inf(lg, f'TwitterAPI認証(API)を終了します。')
    except Exception as e:
        raise(e)
    
    return api


def __get_twitter_api_auth_info() -> dict[Any, Any]:
    '''TwitterAPI認証情報取得'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        twitter_api_auth_info_file: TextIO = open('config/twitter_api_auth_info.json', 'r')
        twitter_api_auth_info: dict[Any, Any] = json.load(twitter_api_auth_info_file)
        
        pyl.log_inf(lg, f'TwitterAPI認証情報取得に成功しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_inf(lg, f'TwitterAPI認証情報取得に失敗しました。')
        raise(e)
    
    return twitter_api_auth_info


def __generate_api(twitter_api_auth_info: dict[Any, Any]) -> tweepy.API:
    '''API生成'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        consumer_key:        str = twitter_api_auth_info['consumer_key']
        consumer_secret:     str = twitter_api_auth_info['consumer_secret']
        access_token:        str = twitter_api_auth_info['access_token']
        access_token_secret: str = twitter_api_auth_info['access_token_secret']
        
        auth: tweepy.OAuthHandler = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        api: tweepy.API = tweepy.API(auth, wait_on_rate_limit=True)
        api.verify_credentials()
        
        pyl.log_inf(lg, f'API生成に成功しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_inf(lg, f'API生成に失敗しました。')
        raise(e)
    
    return api

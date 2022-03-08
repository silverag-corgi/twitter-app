import json
from logging import Logger
from typing import Any, Optional, TextIO

import python_lib_for_me as pyl
import tweepy

from twitter_lib_for_me.util import twitter_api_auth_util


def do_logic_of_api_by_oauth_1_user() -> tweepy.API:
    '''ロジック実行(API生成(OAuth 1.0a User Context))'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'TwitterAPI認証(API生成(OAuth 1.0a User Context))を開始します。')
        
        twitter_api_auth_info: twitter_api_auth_util.TwitterApiAuthInfo = \
            __get_twitter_api_auth_info()
        api: tweepy.API = \
            twitter_api_auth_util.generate_api_by_oauth_1_user(twitter_api_auth_info, True)
        
        pyl.log_inf(lg, f'TwitterAPI認証(API生成(OAuth 1.0a User Context))を終了します。')
    except Exception as e:
        raise(e)
    
    return api


def do_logic_of_api_by_oauth_2_app() -> tweepy.API:
    '''ロジック実行(API生成(OAuth 2.0 App Only))'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'TwitterAPI認証(API生成(OAuth 2.0 App Only))を開始します。')
        
        twitter_api_auth_info: twitter_api_auth_util.TwitterApiAuthInfo = \
            __get_twitter_api_auth_info()
        api: tweepy.API = \
            twitter_api_auth_util.generate_api_by_oauth_2_app(twitter_api_auth_info, True)
        
        pyl.log_inf(lg, f'TwitterAPI認証(API生成(OAuth 2.0 App Only))を終了します。')
    except Exception as e:
        raise(e)
    
    return api


def __get_twitter_api_auth_info() -> twitter_api_auth_util.TwitterApiAuthInfo:
    '''TwitterAPI認証情報取得'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        # TwitterAPI認証情報ファイルの読み込み
        twitter_api_auth_info_file: TextIO = open('config/twitter_api_auth_info.json', 'r')
        twitter_api_auth_info_dict: dict[Any, Any] = json.load(twitter_api_auth_info_file)
        
        # コンシューマーキーの取得
        consumer_keys: dict[Any, Any] = twitter_api_auth_info_dict['consumer_keys']
        api_key:    str = consumer_keys['api_key']
        api_secret: str = consumer_keys['api_secret']
        
        # 認証トークンの取得
        authentication_tokens: dict[Any, Any] = twitter_api_auth_info_dict['authentication_tokens']
        bearer_token:        str = authentication_tokens['bearer_token']
        access_token:        str = authentication_tokens['access_token']
        access_token_secret: str = authentication_tokens['access_token_secret']
        
        # TwitterAPI認証情報の格納
        twitter_api_auth_info: twitter_api_auth_util.TwitterApiAuthInfo = \
            twitter_api_auth_util.TwitterApiAuthInfo(
                    api_key,
                    api_secret,
                    bearer_token,
                    access_token,
                    access_token_secret
                )
        
        pyl.log_inf(lg, f'TwitterAPI認証情報取得に成功しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_inf(lg, f'TwitterAPI認証情報取得に失敗しました。')
        raise(e)
    
    return twitter_api_auth_info

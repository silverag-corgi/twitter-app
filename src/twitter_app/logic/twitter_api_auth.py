import json
from logging import Logger
from typing import Optional, TextIO

import python_lib_for_me as pyl
import tweepy

from twitter_app.util import const_util
from twitter_app.util.twitter_api_v1_1 import twitter_api_auth_util


def do_logic_that_generate_api_by_oauth_1_user() -> tweepy.API:
    '''ロジック実行(TwitterAPI認証)(OAuth 1.0a - User Access Tokens)'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'TwitterAPI認証を開始します。')
        
        twitter_api_auth_info: twitter_api_auth_util.TwitterApiAuthInfo = \
            __get_twitter_api_auth_info()
        api: tweepy.API = twitter_api_auth_util.generate_api_by_oauth_1_user(
            twitter_api_auth_info, True)
    except Exception as e:
        raise(e)
    finally:
        pyl.log_inf(lg, f'TwitterAPI認証を終了します。')
    
    return api


def do_logic_that_generate_api_by_oauth_1_user_using_pin() -> tweepy.API:
    '''ロジック実行(TwitterAPI認証)(OAuth 1.0a - User Access Tokens (PIN-Based OAuth flow))'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'TwitterAPI認証を開始します。')
        
        # TwitterAPI認証情報の取得
        twitter_api_auth_info: twitter_api_auth_util.TwitterApiAuthInfo = \
            __get_twitter_api_auth_info()
        
        # APIの生成
        api: tweepy.API
        api, twitter_api_auth_info = twitter_api_auth_util.generate_api_by_oauth_1_user_using_pin(
            twitter_api_auth_info, True)
        
        # TwitterAPI認証情報の保存
        json.dump(
                twitter_api_auth_info.twitter_api_auth_info_dict,
                open(const_util.TWITTER_API_AUTH_INFO_FILE_PATH, 'w'),
                indent=2
            )
    except Exception as e:
        raise(e)
    finally:
        pyl.log_inf(lg, f'TwitterAPI認証を終了します。')
    
    return api


def do_logic_that_generate_api_by_oauth_2_app() -> tweepy.API:
    '''ロジック実行(TwitterAPI認証)(OAuth 2.0 - Bearer Token (App-Only))'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'TwitterAPI認証を開始します。')
        
        twitter_api_auth_info: twitter_api_auth_util.TwitterApiAuthInfo = \
            __get_twitter_api_auth_info()
        api: tweepy.API = twitter_api_auth_util.generate_api_by_oauth_2_app(
            twitter_api_auth_info, True)
    except Exception as e:
        raise(e)
    finally:
        pyl.log_inf(lg, f'TwitterAPI認証を終了します。')
    
    return api


def __get_twitter_api_auth_info() -> twitter_api_auth_util.TwitterApiAuthInfo:
    '''TwitterAPI認証情報取得'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        # TwitterAPI認証情報ファイルの読み込み
        twitter_api_auth_info_file: TextIO = open(const_util.TWITTER_API_AUTH_INFO_FILE_PATH, 'r')
        twitter_api_auth_info_dict: dict[str, dict] = json.load(twitter_api_auth_info_file)
        
        # TwitterAPI認証情報の生成
        twitter_api_auth_info: twitter_api_auth_util.TwitterApiAuthInfo = \
            twitter_api_auth_util.TwitterApiAuthInfo(twitter_api_auth_info_dict)
        
        pyl.log_inf(lg, f'TwitterAPI認証情報取得に成功しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_inf(lg, f'TwitterAPI認証情報取得に失敗しました。')
        raise(e)
    
    return twitter_api_auth_info

from logging import Logger
from typing import Optional

import python_lib_for_me as pyl
import tweepy


class TwitterApiAuthInfo():
    '''TwitterAPI認証情報'''
    
    def __init__(
            self,
            api_key: str = '',
            api_secret: str = '',
            bearer_token: str = '',
            access_token: str = '',
            access_token_secret: str = ''
        ) -> None:
        self.__api_key = api_key
        self.__api_secret = api_secret
        self.__bearer_token = bearer_token
        self.__access_token = access_token
        self.__access_token_secret = access_token_secret
    
    @property
    def api_key(self) -> str:
        return self.__api_key
    
    @api_key.setter
    def api_key(self, api_key: str) -> None:
        self.__api_key = api_key
    
    @property
    def api_secret(self) -> str:
        return self.__api_secret
    
    @api_secret.setter
    def api_secret(self, api_secret: str) -> None:
        self.__api_secret = api_secret
    
    @property
    def bearer_token(self) -> str:
        return self.__bearer_token
    
    @bearer_token.setter
    def bearer_token(self, bearer_token: str) -> None:
        self.__bearer_token = bearer_token
    
    @property
    def access_token(self) -> str:
        return self.__access_token
    
    @access_token.setter
    def access_token(self, access_token: str) -> None:
        self.__access_token = access_token
    
    @property
    def access_token_secret(self) -> str:
        return self.__access_token_secret
    
    @access_token_secret.setter
    def access_token_secret(self, access_token_secret: str) -> None:
        self.__access_token_secret = access_token_secret


def generate_api_by_oauth_1_user(
        twitter_api_auth_info: TwitterApiAuthInfo,
        wait_on_rate_limit: bool
    ) -> tweepy.API:
    
    '''
    API生成(OAuth 1.0a User Context)
    
    Args:
        twitter_api_auth_info (TwitterApiAuthInfo)  : TwitterAPI認証情報
        wait_on_rate_limit (bool)                   : レート制限時待機有無
    
    Returns:
        tweepy.API: API
    
    Notes:
        - Twitter API v1.1 を OAuth 1.0a の権限で実行する場合に使用する
        - OAuth 1.0a は認証されたTwitter開発者アプリがTwitterアカウントの代わりに以下を行うことを許可する
            - プライベートなアカウント情報へアクセスする
            - Twitterのアクションを実行する
    
    References:
        - https://developer.twitter.com/en/docs/authentication/overview
        - https://developer.twitter.com/en/docs/authentication/oauth-1-0a
    '''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        auth: tweepy.OAuth1UserHandler = tweepy.OAuth1UserHandler(
                twitter_api_auth_info.api_key,
                twitter_api_auth_info.api_secret,
                twitter_api_auth_info.access_token,
                twitter_api_auth_info.access_token_secret
            )
        api: tweepy.API = tweepy.API(auth, wait_on_rate_limit=wait_on_rate_limit)
        api.verify_credentials()
        
        pyl.log_inf(lg, f'API生成(OAuth 1.0a User Context)に成功しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_inf(lg, f'API生成(OAuth 1.0a User Context)に失敗しました。')
        raise(e)
    
    return api


def generate_api_by_oauth_2_app(
        twitter_api_auth_info: TwitterApiAuthInfo,
        wait_on_rate_limit: bool
    ) -> tweepy.API:
    
    '''
    API生成(OAuth 2.0 App Only)
    
    Args:
        twitter_api_auth_info (TwitterApiAuthInfo)  : TwitterAPI認証情報
        wait_on_rate_limit (bool)                   : レート制限時待機有無
    
    Returns:
        tweepy.API: API
    
    Notes:
        - Twitter API v1.1 を OAuth 2.0 の権限で実行する場合に使用する
        - OAuth 2.0 はTwitter開発者向けアプリが以下を行うことを許可する
            - Twitterで公開されている情報に読み取り専用でアクセスする
    
    References:
        - https://developer.twitter.com/en/docs/authentication/overview
        - https://developer.twitter.com/en/docs/authentication/oauth-2-0
    '''
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        auth: tweepy.OAuth2AppHandler = tweepy.OAuth2AppHandler(
                twitter_api_auth_info.api_key,
                twitter_api_auth_info.api_secret
            )
        api: tweepy.API = tweepy.API(auth, wait_on_rate_limit=wait_on_rate_limit)
        
        pyl.log_inf(lg, f'API生成(OAuth 2.0 App Only)に成功しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_inf(lg, f'API生成(OAuth 2.0 App Only)に失敗しました。')
        raise(e)
    
    return api

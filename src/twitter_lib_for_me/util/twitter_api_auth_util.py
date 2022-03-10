import webbrowser
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl
import tweepy


class TwitterApiAuthInfo():
    '''TwitterAPI認証情報'''
    
    def __init__(
            self,
            twitter_api_auth_info_dict: dict[str, dict]
        ) -> None:
        
        '''
        コンストラクタ
        
        Args:
            twitter_api_auth_info_dict (dict[str, dict]): TwitterAPI認証情報辞書
        '''
        
        # コンシューマーキーの取得
        consumer_keys: dict[str, str] = twitter_api_auth_info_dict['consumer_keys']
        api_key:    str = consumer_keys['api_key']
        api_secret: str = consumer_keys['api_secret']
        
        # 認証トークンの取得
        authentication_tokens: dict[str, str] = twitter_api_auth_info_dict['authentication_tokens']
        bearer_token:           str = authentication_tokens['bearer_token']
        access_token:           str = authentication_tokens['access_token']
        access_token_secret:    str = authentication_tokens['access_token_secret']
        
        # インスタンス変数への格納
        self.__twitter_api_auth_info_dict = twitter_api_auth_info_dict
        self.__api_key = api_key
        self.__api_secret = api_secret
        self.__bearer_token = bearer_token
        self.__access_token = access_token
        self.__access_token_secret = access_token_secret
    
    @property
    def twitter_api_auth_info_dict(self) -> dict[str, dict]:
        return self.__twitter_api_auth_info_dict
    
    @twitter_api_auth_info_dict.setter
    def twitter_api_auth_info_dict(self, twitter_api_auth_info_dict: dict[str, dict]) -> None:
        self.__twitter_api_auth_info_dict = twitter_api_auth_info_dict
    
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
        self.__twitter_api_auth_info_dict['authentication_tokens']['bearer_token'] = bearer_token
        self.__bearer_token = bearer_token
    
    @property
    def access_token(self) -> str:
        return self.__access_token
    
    @access_token.setter
    def access_token(self, access_token: str) -> None:
        self.__twitter_api_auth_info_dict['authentication_tokens']['access_token'] = access_token
        self.__access_token = access_token
    
    @property
    def access_token_secret(self) -> str:
        return self.__access_token_secret
    
    @access_token_secret.setter
    def access_token_secret(self, access_token_secret: str) -> None:
        self.__twitter_api_auth_info_dict['authentication_tokens']['access_token_secret'] = \
            access_token_secret
        self.__access_token_secret = access_token_secret


def generate_api_by_oauth_1_user(
        twitter_api_auth_info: TwitterApiAuthInfo,
        wait_on_rate_limit: bool
    ) -> tweepy.API:
    
    '''
    API生成(OAuth 1.0a - User Access Tokens)
    
    Args:
        twitter_api_auth_info (TwitterApiAuthInfo)  : TwitterAPI認証情報
        wait_on_rate_limit (bool)                   : レート制限時待機有無
    
    Returns:
        tweepy.API: API
    
    Notes:
        - ユーザ認証(OAuth 1.0a)を使用して Twitter API v1.1 を実行する場合に使用する
        - ユーザ認証(OAuth 1.0a)は認証されたTwitter開発者アプリがTwitterアカウントの代わりに以下を行うことを許可する
            - プライベートなアカウント情報へアクセスする
            - Twitterのアクションを実行する
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/authentication/overview
            - https://developer.twitter.com/en/docs/authentication/oauth-1-0a
    '''  # noqa: E501
    
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
        
        pyl.log_inf(lg, f'API生成(OAuth 1.0a - User Access Tokens)に成功しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'API生成(OAuth 1.0a - User Access Tokens)に失敗しました。')
        raise(e)
    
    return api


def generate_api_by_oauth_1_user_using_pin(
        twitter_api_auth_info: TwitterApiAuthInfo,
        wait_on_rate_limit: bool
    ) -> tuple[tweepy.API, TwitterApiAuthInfo]:
    
    '''
    API生成(OAuth 1.0a - User Access Tokens (PIN-Based OAuth flow))
    
    Args:
        twitter_api_auth_info (TwitterApiAuthInfo)  : TwitterAPI認証情報
        wait_on_rate_limit (bool)                   : レート制限時待機有無
    
    Returns:
        tuple[tweepy.API, TwitterApiAuthInfo]: API, TwitterAPI認証情報
    
    Notes:
        - ユーザ認証(OAuth 1.0a)を使用して Twitter API v1.1 を実行する場合に使用する
        - ユーザ認証(OAuth 1.0a)は認証されたTwitter開発者アプリがTwitterアカウントの代わりに以下を行うことを許可する
            - プライベートなアカウント情報へアクセスする
            - Twitterのアクションを実行する
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/authentication/overview
            - https://developer.twitter.com/en/docs/authentication/oauth-1-0a/pin-based-oauth
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        # 認証情報の設定(帯域外認証：Out of Band)
        auth: tweepy.OAuth1UserHandler = tweepy.OAuth1UserHandler(
                twitter_api_auth_info.api_key,
                twitter_api_auth_info.api_secret,
                callback='oob'
            )
        
        # PINコードの生成・入力
        authorization_url: str = auth.get_authorization_url()
        webbrowser.open(authorization_url)
        pin_code: str = input('PINコードを入力してください : ')
        
        # アクセストークンの生成
        auth.get_access_token(pin_code)
        twitter_api_auth_info.access_token = str(auth.access_token)
        twitter_api_auth_info.access_token_secret = str(auth.access_token_secret)
        
        # APIの生成
        api: tweepy.API = tweepy.API(auth, wait_on_rate_limit=wait_on_rate_limit)
        api.verify_credentials()
        
        pyl.log_inf(lg, f'API生成(OAuth 1.0a - User Access Tokens (PIN-Based OAuth flow))' +
                        f'に成功しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'API生成(OAuth 1.0a - User Access Tokens (PIN-Based OAuth flow))' +
                            f'に失敗しました。')
        raise(e)
    
    return api, twitter_api_auth_info


def generate_api_by_oauth_2_app(
        twitter_api_auth_info: TwitterApiAuthInfo,
        wait_on_rate_limit: bool
    ) -> tweepy.API:
    
    '''
    API生成(OAuth 2.0 - Bearer Token (App-Only))
    
    Args:
        twitter_api_auth_info (TwitterApiAuthInfo)  : TwitterAPI認証情報
        wait_on_rate_limit (bool)                   : レート制限時待機有無
    
    Returns:
        tweepy.API: API
    
    Notes:
        - アプリ認証(OAuth 2.0)を使用して Twitter API v1.1 を実行する場合に使用する
        - アプリ認証(OAuth 2.0)はTwitter開発者向けアプリが以下を行うことを許可する
            - Twitterで公開されている情報に読み取り専用(Getメソッド)でアクセスする
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/authentication/overview
            - https://developer.twitter.com/en/docs/authentication/oauth-2-0
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        auth: tweepy.OAuth2AppHandler = tweepy.OAuth2AppHandler(
                twitter_api_auth_info.api_key,
                twitter_api_auth_info.api_secret
            )
        api: tweepy.API = tweepy.API(auth, wait_on_rate_limit=wait_on_rate_limit)
        
        pyl.log_inf(lg, f'API生成(OAuth 2.0 - Bearer Token (App-Only))に成功しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'API生成(OAuth 2.0 - Bearer Token (App-Only))に失敗しました。')
        raise(e)
    
    return api

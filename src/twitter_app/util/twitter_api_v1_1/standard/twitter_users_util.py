import math
from enum import IntEnum
from logging import Logger
from typing import Any, Optional

import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet

####################################################################################################
# Follow, search, and get users
####################################################################################################


class EnumOfFollowee():
    class EnumOfOauth1User(IntEnum):
        MAX_NUM_OF_DATA_PER_REQUEST = 200
        MAX_NUM_OF_REQUESTS_PER_15MIN = 15
        MAX_NUM_OF_DATA_PER_15MIN = MAX_NUM_OF_DATA_PER_REQUEST * MAX_NUM_OF_REQUESTS_PER_15MIN
    
    class EnumOfOauth2App(IntEnum):
        MAX_NUM_OF_DATA_PER_REQUEST = 200
        MAX_NUM_OF_REQUESTS_PER_15MIN = 15
        MAX_NUM_OF_DATA_PER_15MIN = MAX_NUM_OF_DATA_PER_REQUEST * MAX_NUM_OF_REQUESTS_PER_15MIN


def get_followee_pages(
        api: tweepy.API,
        twitter_user_id: str,
        num_of_data: int = EnumOfFollowee.EnumOfOauth1User.MAX_NUM_OF_DATA_PER_15MIN.value,
        num_of_data_per_request: int =
        EnumOfFollowee.EnumOfOauth1User.MAX_NUM_OF_DATA_PER_REQUEST.value
    ) -> list[ResultSet]:
    
    '''
    フォロイーページ取得
    
    Args:
        api (tweepy.API)                        : API
        twitter_user_id (str)                   : TwitterユーザID
        num_of_data (int, optional)             : データ数
        num_of_data_per_request (int, optional) : リクエストごとのデータ数
    
    Returns:
        list[ResultSet] : フォロイーページ (list[ResultSet[tweepy.models.User]])
    
    Notes:
        - 認証
            - ユーザ認証(OAuth 1.0a)
            - アプリ認証(OAuth 2.0)
        - エンドポイント
            - GET friends/list
        - レート制限
            - ユーザ認証(OAuth 1.0a)
                - データ数／リクエスト : 200
                - リクエスト数／１５分 : 15
                    - 超過した場合は15分の待機時間が発生する
            - アプリ認証(OAuth 2.0)
                - データ数／リクエスト : 200
                - リクエスト数／１５分 : 15
                    - 超過した場合は15分の待機時間が発生する
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-friends-list
        - レスポンス
            - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    followee_pages: list[ResultSet] = []
    
    # 認証方式の確認
    if not (isinstance(api.auth, tweepy.OAuth1UserHandler) == True
            or isinstance(api.auth, tweepy.OAuth2AppHandler) == True):
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
        
        # リクエスト数の算出
        num_of_requests = math.ceil(num_of_data / num_of_data_per_request)
        
        # フォロイーページの取得
        followee_pagination: tweepy.Cursor = tweepy.Cursor(
                api.get_friends,
                screen_name=twitter_user_id,
                count=num_of_data_per_request
            )
        followee_pages = list(followee_pagination.pages(num_of_requests))
        
        pyl.log_inf(lg, f'フォロイーページ取得に成功しました。(twitter_user_id:{twitter_user_id})')
    except Exception as e:
        if lg is not None:
            pyl.log_war(lg, f'フォロイーページ取得に失敗しました。(twitter_user_id:{twitter_user_id})', e)
    
    return followee_pages


class EnumOfFollower():
    class EnumOfOauth1User(IntEnum):
        MAX_NUM_OF_DATA_PER_REQUEST = 200
        MAX_NUM_OF_REQUESTS_PER_15MIN = 15
        MAX_NUM_OF_DATA_PER_15MIN = MAX_NUM_OF_DATA_PER_REQUEST * MAX_NUM_OF_REQUESTS_PER_15MIN
    
    class EnumOfOauth2App(IntEnum):
        MAX_NUM_OF_DATA_PER_REQUEST = 200
        MAX_NUM_OF_REQUESTS_PER_15MIN = 15
        MAX_NUM_OF_DATA_PER_15MIN = MAX_NUM_OF_DATA_PER_REQUEST * MAX_NUM_OF_REQUESTS_PER_15MIN


def get_follower_pages(
        api: tweepy.API,
        twitter_user_id: str,
        num_of_data: int = EnumOfFollower.EnumOfOauth1User.MAX_NUM_OF_DATA_PER_15MIN.value,
        num_of_data_per_request: int =
        EnumOfFollower.EnumOfOauth1User.MAX_NUM_OF_DATA_PER_REQUEST.value
    ) -> list[ResultSet]:
    
    '''
    フォロワーページ取得
    
    Args:
        api (tweepy.API)                        : API
        twitter_user_id (str)                   : TwitterユーザID
        num_of_data (int, optional)             : データ数
        num_of_data_per_request (int, optional) : リクエストごとのデータ数
    
    Returns:
        list[ResultSet] : フォロワーページ (list[ResultSet[tweepy.models.User]])
    
    Notes:
        - 認証
            - ユーザ認証(OAuth 1.0a)
            - アプリ認証(OAuth 2.0)
        - エンドポイント
            - GET followers/list
        - レート制限
            - ユーザ認証(OAuth 1.0a)
                - データ数／リクエスト : 200
                - リクエスト数／１５分 : 15
                    - 超過した場合は15分の待機時間が発生する
            - アプリ認証(OAuth 2.0)
                - データ数／リクエスト : 200
                - リクエスト数／１５分 : 15
                    - 超過した場合は15分の待機時間が発生する
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-followers-list
        - レスポンス
            - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    follower_pages: list[ResultSet] = []
    
    # 認証方式の確認
    if not (isinstance(api.auth, tweepy.OAuth1UserHandler) == True
            or isinstance(api.auth, tweepy.OAuth2AppHandler) == True):
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
        
        # リクエスト数の算出
        num_of_requests = math.ceil(num_of_data / num_of_data_per_request)
        
        # フォロワーページの取得
        follower_pagination: tweepy.Cursor = tweepy.Cursor(
                api.get_followers,
                screen_name=twitter_user_id,
                count=num_of_data_per_request
            )
        follower_pages = list(follower_pagination.pages(num_of_requests))
        
        pyl.log_inf(lg, f'フォロワーページ取得に成功しました。(twitter_user_id:{twitter_user_id})')
    except Exception as e:
        if lg is not None:
            pyl.log_war(lg, f'フォロワーページ取得に失敗しました。(twitter_user_id:{twitter_user_id})', e)
    
    return follower_pages


def get_user_info(
        api: tweepy.API,
        twitter_user_id: str
    ) -> Any:
    
    '''
    ユーザ情報取得
    
    Args:
        api (tweepy.API)        : API
        twitter_user_id (str)   : TwitterユーザID
    
    Returns:
        Any: ユーザ情報 (tweepy.models.User)
    
    Notes:
        - 認証
            - ユーザ認証(OAuth 1.0a)
            - アプリ認証(OAuth 2.0)
        - エンドポイント
            - GET users/show
        - レート制限
            - ユーザ認証(OAuth 1.0a)
                - リクエスト数／１５分 : 900
                    - 超過した場合は15分の待機時間が発生する
            - アプリ認証(OAuth 2.0)
                - リクエスト数／１５分 : 900
                    - 超過した場合は15分の待機時間が発生する
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-users-show
        - レスポンス
            - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    # 認証方式の確認
    if not (isinstance(api.auth, tweepy.OAuth1UserHandler) == True
            or isinstance(api.auth, tweepy.OAuth2AppHandler) == True):
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        
        # ユーザ情報の取得
        user_info: Any = api.get_user(screen_name=twitter_user_id)
        
        pyl.log_deb(lg, f'ユーザ情報取得に成功しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'ユーザ情報取得に失敗しました。')
        raise(e)
    
    return user_info


####################################################################################################
# Create and manage lists
####################################################################################################


def get_twitter_lists(
        api: tweepy.API,
        twitter_user_id: str = ''
    ) -> ResultSet:
    
    '''
    Twitterリスト一覧取得
    
    Args:
        api (tweepy.API)        : API
        twitter_user_id (str)   : TwitterユーザID
    
    Returns:
        ResultSet: Twitterリスト一覧 (ResultSet[tweepy.models.List])
    
    Notes:
        - 認証
            - ユーザ認証(OAuth 1.0a)
            - アプリ認証(OAuth 2.0)
        - エンドポイント
            - GET lists/list
        - レート制限
            - ユーザ認証(OAuth 1.0a)
                - リクエスト数／１５分 : 15
                    - 超過した場合は15分の待機時間が発生する
            - アプリ認証(OAuth 2.0)
                - リクエスト数／１５分 : 15
                    - 超過した場合は15分の待機時間が発生する
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-list
        - レスポンス
            - https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/lists
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-show#example-response
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    # 認証方式の確認
    if not (isinstance(api.auth, tweepy.OAuth1UserHandler) == True
            or isinstance(api.auth, tweepy.OAuth2AppHandler) == True):
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        
        # Twitterリスト一覧の取得
        twitter_lists: Any
        if twitter_user_id == '':
            twitter_lists = api.get_lists(reverse=True)
        else:
            twitter_lists = api.get_lists(screen_name=twitter_user_id, reverse=True)
        
        pyl.log_inf(lg, f'Twitterリスト一覧取得に成功しました。(twitter_user_id:{twitter_user_id})')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'Twitterリスト一覧取得に失敗しました。(twitter_user_id:{twitter_user_id})')
        raise(e)
    
    return twitter_lists


class EnumOfTwitterListMember():
    class EnumOfOauth1User(IntEnum):
        MAX_NUM_OF_DATA_PER_REQUEST = 5000
        MAX_NUM_OF_REQUESTS_PER_15MIN = 900
        MAX_NUM_OF_DATA_PER_15MIN = MAX_NUM_OF_DATA_PER_REQUEST * MAX_NUM_OF_REQUESTS_PER_15MIN
    
    class EnumOfOauth2App(IntEnum):
        MAX_NUM_OF_DATA_PER_REQUEST = 5000
        MAX_NUM_OF_REQUESTS_PER_15MIN = 75
        MAX_NUM_OF_DATA_PER_15MIN = MAX_NUM_OF_DATA_PER_REQUEST * MAX_NUM_OF_REQUESTS_PER_15MIN


def get_twitter_list_member_pages(
        api: tweepy.API,
        twitter_list_id: str,
        num_of_data: int = EnumOfTwitterListMember.EnumOfOauth1User.MAX_NUM_OF_DATA_PER_15MIN.value,
        num_of_data_per_request: int =
        EnumOfTwitterListMember.EnumOfOauth1User.MAX_NUM_OF_DATA_PER_REQUEST.value
    ) -> list[ResultSet]:
    
    '''
    Twitterリストメンバーページ取得
    
    Args:
        api (tweepy.API)                        : API
        twitter_list_id (str)                   : TwitterリストID
        num_of_data (int, optional)             : データ数
        num_of_data_per_request (int, optional) : リクエストごとのデータ数
    
    Returns:
        list[ResultSet] : Twitterリストメンバーページ (list[ResultSet[tweepy.models.User]])
    
    Notes:
        - 認証
            - ユーザ認証(OAuth 1.0a)
            - アプリ認証(OAuth 2.0)
        - エンドポイント
            - GET lists/members
        - レート制限
            - ユーザ認証(OAuth 1.0a)
                - データ数／リクエスト : 5000
                - リクエスト数／１５分 : 900
                    - 超過した場合は15分の待機時間が発生する
            - アプリ認証(OAuth 2.0)
                - データ数／リクエスト : 5000
                - リクエスト数／１５分 : 75
                    - 超過した場合は15分の待機時間が発生する
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-members
        - レスポンス
            - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    twitter_list_member_pages: list[ResultSet] = []
    
    # 認証方式の確認
    if not (isinstance(api.auth, tweepy.OAuth1UserHandler) == True
            or isinstance(api.auth, tweepy.OAuth2AppHandler) == True):
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
        
        # リクエスト数の算出
        num_of_requests = math.ceil(num_of_data / num_of_data_per_request)
        
        # Twitterリストメンバーページの取得
        twitter_list_member_pagination: tweepy.Cursor = tweepy.Cursor(
                api.get_list_members,
                list_id=twitter_list_id,
                count=num_of_data_per_request
            )
        twitter_list_member_pages = list(twitter_list_member_pagination.pages(num_of_requests))
        
        pyl.log_inf(lg, f'Twitterリストメンバーページ取得に成功しました。' +
                        f'(twitter_list_id:{twitter_list_id})')
    except Exception as e:
        if lg is not None:
            pyl.log_war(lg, f'Twitterリストメンバーページ取得に失敗しました。' +
                            f'(twitter_list_id:{twitter_list_id})', e)
    
    return twitter_list_member_pages


def generate_twitter_list(
        api: tweepy.API,
        twitter_list_name: str
    ) -> Any:
    
    '''
    Twitterリスト生成
    
    Args:
        api (tweepy.API)        : API
        twitter_list_name (str) : Twitterリスト名
    
    Returns:
        Any: Twitterリスト (tweepy.models.List)
    
    Notes:
        - 認証
            - ユーザ認証(OAuth 1.0a)
        - エンドポイント
            - POST lists/create
        - レート制限
            - ユーザ認証(OAuth 1.0a)
                - リクエスト数／１５分 : (未公表)
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/post-lists-create
        - レスポンス
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-show#example-response
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    # 認証方式の確認
    if not (isinstance(api.auth, tweepy.OAuth1UserHandler) == True):
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        
        # Twitterリストの生成
        twitter_list: Any = api.create_list(twitter_list_name, mode='private', description='')
        
        pyl.log_inf(lg, f'Twitterリスト生成に成功しました。(twitter_list_name:{twitter_list_name})')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'Twitterリスト生成に失敗しました。' +
                            f'(twitter_list_name:{twitter_list_name})')
        raise(e)
    
    return twitter_list


def destroy_twitter_list(
        api: tweepy.API,
        twitter_list_name: str
    ) -> bool:
    
    '''
    Twitterリスト破棄
    
    Args:
        api (tweepy.API)        : API
        twitter_list_name (str) : Twitterリスト名
    
    Returns:
        bool: 実行結果 (True：成功、False：失敗)
    
    Notes:
        - 認証
            - ユーザ認証(OAuth 1.0a)
        - エンドポイント
            - POST lists/destroy
        - レート制限
            - ユーザ認証(OAuth 1.0a)
                - リクエスト数／１５分 : (未公表)
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/post-lists-destroy
        - レスポンス
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-show#example-response
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    result: bool = False
    
    # 認証方式の確認
    if not (isinstance(api.auth, tweepy.OAuth1UserHandler) == True):
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        
        # Twitterリスト一覧の取得
        twitter_lists: ResultSet = get_twitter_lists(api)
        
        # Twitterリストの破棄
        for twitter_list in twitter_lists:
            if twitter_list.name == twitter_list_name:
                api.destroy_list(list_id=twitter_list.id)
                pyl.log_inf(lg, f'Twitterリスト破棄に成功しました。' +
                                f'(twitter_list_name:{twitter_list_name})')
                result = True
                break
    except Exception as e:
        if lg is not None:
            pyl.log_war(lg, f'Twitterリスト破棄に失敗しました。' +
                            f'(twitter_list_name:{twitter_list_name})', e)
    
    return result


def add_twitter_user_to_twitter_list(
        api: tweepy.API,
        twitter_list_id: str,
        twitter_user_id: str,
        twitter_user_name: str = ''
    ) -> bool:
    
    '''
    Twitterユーザ追加
    
    Args:
        api (tweepy.API)                    : API
        twitter_list_id (str)               : TwitterリストID
        twitter_user_id (str)               : TwitterユーザID
        twitter_user_name (str, optional)   : Twitterユーザ名
    
    Returns:
        bool: 実行結果 (True：成功、False：失敗)
    
    Notes:
        - 認証
            - ユーザ認証(OAuth 1.0a)
        - エンドポイント
            - POST lists/members/create
        - レート制限
            - ユーザ認証(OAuth 1.0a)
                - リクエスト数／１５分 : (未公表)
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/post-lists-members-create
        - レスポンス
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-show#example-response
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    result: bool = False
    
    # 認証方式の確認
    if not (isinstance(api.auth, tweepy.OAuth1UserHandler) == True):
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        
        # Twitterユーザの追加
        api.add_list_member(list_id=twitter_list_id, screen_name=twitter_user_id)
        pyl.log_deb(lg, f'Twitterユーザ追加に成功しました。' +
                        f'(twitter_user_id:{twitter_user_id: <15}, ' +
                        f'twitter_user_name:{twitter_user_name})')
        
        result = True
    except Exception as e:
        if lg is not None:
            pyl.log_war(lg, f'Twitterユーザ追加に失敗しました。鍵付きや削除済みの可能性があります。' +
                            f'(twitter_user_id:{twitter_user_id: <15}, ' +
                            f'twitter_user_name:{twitter_user_name})', e)
    
    return result


####################################################################################################
# Manage account settings and profile
####################################################################################################


def get_auth_user_info(
        api: tweepy.API,
    ) -> Any:
    
    '''
    認証ユーザ情報取得
    
    Args:
        api (tweepy.API) : API
    
    Returns:
        Any: 認証ユーザ情報 (tweepy.models.User)
    
    Notes:
        - 認証
            - ユーザ認証(OAuth 1.0a)
        - エンドポイント
            - GET account/verify_credentials
        - レート制限
            - ユーザ認証(OAuth 1.0a)
                - リクエスト数／１５分 : (未公表)
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/manage-account-settings/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/manage-account-settings/api-reference/get-account-verify_credentials
        - レスポンス
            - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    # 認証方式の確認
    if not (isinstance(api.auth, tweepy.OAuth1UserHandler) == True):
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        
        # 認証ユーザ情報の取得
        auth_user_info : Any = api.verify_credentials()
        
        pyl.log_inf(lg, f'認証ユーザ情報取得に成功しました。' +
                        f'(twitter_user_id:{auth_user_info.screen_name: <15}, ' +
                        f'twitter_user_name:{auth_user_info.name})')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'認証ユーザ情報取得に失敗しました。')
        raise(e)
    
    return auth_user_info

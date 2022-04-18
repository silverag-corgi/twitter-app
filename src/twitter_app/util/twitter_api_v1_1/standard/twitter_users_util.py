import math
import time
from datetime import datetime, timedelta
from enum import IntEnum
from logging import Logger
from typing import Any, Optional

import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet

from twitter_app import util

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
        user_id: str,
        num_of_data: int = EnumOfFollowee.EnumOfOauth1User.MAX_NUM_OF_DATA_PER_15MIN.value,
        num_of_data_per_request: int =
        EnumOfFollowee.EnumOfOauth1User.MAX_NUM_OF_DATA_PER_REQUEST.value
    ) -> list[ResultSet]:
    
    '''
    フォロイーページ取得
    
    Args:
        api (tweepy.API)                        : API
        user_id (str)                           : ユーザID
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
    if isinstance(api.auth, (tweepy.OAuth1UserHandler, tweepy.OAuth2AppHandler)) == False:
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
                screen_name=user_id,
                count=num_of_data_per_request
            )
        followee_pages = list(followee_pagination.pages(num_of_requests))
        
        pyl.log_inf(lg, f'フォロイーページ取得に成功しました。(user_id:{user_id})')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'フォロイーページ取得に失敗しました。(user_id:{user_id})')
        raise(e)
    
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
        user_id: str,
        num_of_data: int = EnumOfFollower.EnumOfOauth1User.MAX_NUM_OF_DATA_PER_15MIN.value,
        num_of_data_per_request: int =
        EnumOfFollower.EnumOfOauth1User.MAX_NUM_OF_DATA_PER_REQUEST.value
    ) -> list[ResultSet]:
    
    '''
    フォロワーページ取得
    
    Args:
        api (tweepy.API)                        : API
        user_id (str)                           : ユーザID
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
    if isinstance(api.auth, (tweepy.OAuth1UserHandler, tweepy.OAuth2AppHandler)) == False:
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
                screen_name=user_id,
                count=num_of_data_per_request
            )
        follower_pages = list(follower_pagination.pages(num_of_requests))
        
        pyl.log_inf(lg, f'フォロワーページ取得に成功しました。(user_id:{user_id})')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'フォロワーページ取得に失敗しました。(user_id:{user_id})')
        raise(e)
    
    return follower_pages


def get_friendship(
        api: tweepy.API,
        user_id_source: str,
        user_id_target: str
    ) -> Any:
    
    '''
    交友関係取得
    
    Args:
        api (tweepy.API)        : API
        user_id_source (str)    : ユーザID(比較元)
        user_id_target (str)    : ユーザID(比較対象)
    
    Returns:
        Any: 交友関係 (tweepy.models.Friendship)
    
    Notes:
        - 認証
            - ユーザ認証(OAuth 1.0a)
            - アプリ認証(OAuth 2.0)
        - エンドポイント
            - GET friendships/show
        - レート制限
            - ユーザ認証(OAuth 1.0a)
                - リクエスト数／１５分 : 180
                    - 超過した場合は15分の待機時間が発生する
            - アプリ認証(OAuth 2.0)
                - リクエスト数／１５分 : 15
                    - 超過した場合は15分の待機時間が発生する
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-friendships-show
        - レスポンス
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-friendships-show#example-response
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    # 認証方式の確認
    if isinstance(api.auth, (tweepy.OAuth1UserHandler, tweepy.OAuth2AppHandler)) == False:
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        
        # 交友関係の取得
        friendship: Any = api.get_friendship(
            source_screen_name=user_id_source, target_screen_name=user_id_target)
        
        pyl.log_deb(lg, f'交友関係取得に成功しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'交友関係取得に失敗しました。')
        raise(e)
    
    return friendship


class EnumOfUserForLookup(IntEnum):
    MAX_NUM_OF_DATA_PER_REQUEST = 100


def lookup_users(
        api: tweepy.API,
        user_ids: list[str],
        num_of_data_per_request: int = EnumOfUserForLookup.MAX_NUM_OF_DATA_PER_REQUEST.value
    ) -> list[ResultSet]:
    
    '''
    ユーザ検索
    
    Args:
        api (tweepy.API)                        : API
        user_ids (str)                          : ユーザID(複数)
        num_of_data_per_request (int, optional) : リクエストごとのデータ数
    
    Returns:
        list[ResultSet]: ユーザ検索結果ページ (list[ResultSet[tweepy.models.User]])
    
    Notes:
        - 認証
            - ユーザ認証(OAuth 1.0a)
            - アプリ認証(OAuth 2.0)
        - エンドポイント
            - GET users/lookup
        - レート制限
            - ユーザ認証(OAuth 1.0a)
                - データ数／リクエスト : 100
                - リクエスト数／１５分 : 900
                    - 超過した場合は15分の待機時間が発生する
            - アプリ認証(OAuth 2.0)
                - データ数／リクエスト : 100
                - リクエスト数／１５分 : 300
                    - 超過した場合は15分の待機時間が発生する
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-users-lookup
        - レスポンス
            - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    user_pages: list[ResultSet] = []
    
    # 認証方式の確認
    if isinstance(api.auth, (tweepy.OAuth1UserHandler, tweepy.OAuth2AppHandler)) == False:
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        
        # ユーザIDリスト(100人ごと)の生成
        user_ids_list: list[list[str]] = pyl.split_list(user_ids, num_of_data_per_request)
        
        # ユーザ(100人ごと)の検索
        for user_ids_by_element in user_ids_list:
            users: Any = api.lookup_users(screen_name=user_ids_by_element)
            user_pages.append(users)
        
        pyl.log_inf(lg, f'ユーザ検索に成功しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'ユーザ検索に失敗しました。')
        raise(e)
    
    return user_pages


def get_user_info(
        api: tweepy.API,
        user_id: str
    ) -> Any:
    
    '''
    ユーザ情報取得
    
    Args:
        api (tweepy.API)    : API
        user_id (str)       : ユーザID
    
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
    if isinstance(api.auth, (tweepy.OAuth1UserHandler, tweepy.OAuth2AppHandler)) == False:
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        
        # ユーザ情報の取得
        user_info: Any = api.get_user(screen_name=user_id)
        
        pyl.log_deb(lg, f'ユーザ情報取得に成功しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'ユーザ情報取得に失敗しました。')
        raise(e)
    
    return user_info


####################################################################################################
# Create and manage lists
####################################################################################################


def get_lists(
        api: tweepy.API,
        user_id: str = ''
    ) -> ResultSet:
    
    '''
    リスト(複数)取得
    
    Args:
        api (tweepy.API)    : API
        user_id (str)       : ユーザID
    
    Returns:
        ResultSet: リスト(複数) (ResultSet[tweepy.models.List])
    
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
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-show#example-response
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    # 認証方式の確認
    if isinstance(api.auth, (tweepy.OAuth1UserHandler, tweepy.OAuth2AppHandler)) == False:
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        
        # リスト(複数)の取得
        lists: Any
        if user_id == '':
            lists = api.get_lists(reverse=True)
        else:
            lists = api.get_lists(screen_name=user_id, reverse=True)
        
        pyl.log_inf(lg, f'リスト(複数)取得に成功しました。(user_id:{user_id})')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'リスト(複数)取得に失敗しました。(user_id:{user_id})')
        raise(e)
    
    return lists


class EnumOfListMember():
    class EnumOfOauth1User(IntEnum):
        MAX_NUM_OF_DATA_PER_REQUEST = 5000
        MAX_NUM_OF_REQUESTS_PER_15MIN = 900
        MAX_NUM_OF_DATA_PER_15MIN = MAX_NUM_OF_DATA_PER_REQUEST * MAX_NUM_OF_REQUESTS_PER_15MIN
    
    class EnumOfOauth2App(IntEnum):
        MAX_NUM_OF_DATA_PER_REQUEST = 5000
        MAX_NUM_OF_REQUESTS_PER_15MIN = 75
        MAX_NUM_OF_DATA_PER_15MIN = MAX_NUM_OF_DATA_PER_REQUEST * MAX_NUM_OF_REQUESTS_PER_15MIN


def get_list_member_pages(
        api: tweepy.API,
        list_id: str,
        num_of_data: int = EnumOfListMember.EnumOfOauth1User.MAX_NUM_OF_DATA_PER_15MIN.value,
        num_of_data_per_request: int =
        EnumOfListMember.EnumOfOauth1User.MAX_NUM_OF_DATA_PER_REQUEST.value
    ) -> list[ResultSet]:
    
    '''
    リストメンバーページ取得
    
    Args:
        api (tweepy.API)                        : API
        list_id (str)                           : リストID
        num_of_data (int, optional)             : データ数
        num_of_data_per_request (int, optional) : リクエストごとのデータ数
    
    Returns:
        list[ResultSet] : リストメンバーページ (list[ResultSet[tweepy.models.User]])
    
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
    list_member_pages: list[ResultSet] = []
    
    # 認証方式の確認
    if isinstance(api.auth, (tweepy.OAuth1UserHandler, tweepy.OAuth2AppHandler)) == False:
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
        
        # リクエスト数の算出
        num_of_requests = math.ceil(num_of_data / num_of_data_per_request)
        
        # リストメンバーページの取得
        list_member_pagination: tweepy.Cursor = tweepy.Cursor(
                api.get_list_members,
                list_id=list_id,
                count=num_of_data_per_request
            )
        list_member_pages = list(list_member_pagination.pages(num_of_requests))
        
        pyl.log_inf(lg, f'リストメンバーページ取得に成功しました。(list_id:{list_id})')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'リストメンバーページ取得に失敗しました。(list_id:{list_id})')
        raise(e)
    
    return list_member_pages


def generate_list(
        api: tweepy.API,
        list_name: str
    ) -> Any:
    
    '''
    リスト生成
    
    Args:
        api (tweepy.API)    : API
        list_name (str)     : リスト名
    
    Returns:
        Any: リスト (tweepy.models.List)
    
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
    if isinstance(api.auth, (tweepy.OAuth1UserHandler)) == False:
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        
        # リストの生成
        list_: Any = api.create_list(list_name, mode='private', description='')
        
        pyl.log_inf(lg, f'リスト生成に成功しました。(list_name:{list_name})')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'リスト生成に失敗しました。(list_name:{list_name})')
        raise(e)
    
    return list_


def destroy_list(
        api: tweepy.API,
        list_name: str
    ) -> bool:
    
    '''
    リスト破棄
    
    Args:
        api (tweepy.API)    : API
        list_name (str)     : リスト名
    
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
    if isinstance(api.auth, (tweepy.OAuth1UserHandler)) == False:
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        
        # リスト(複数)の取得
        lists: ResultSet = get_lists(api)
        
        # リストの破棄
        for list in lists:
            if list.name == list_name:
                api.destroy_list(list_id=list.id)
                pyl.log_inf(lg, f'リスト破棄に成功しました。(list_name:{list_name})')
                result = True
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'リスト破棄に失敗しました。(list_name:{list_name})')
        raise(e)
    
    return result


class EnumOfUserForList(IntEnum):
    MAX_NUM_OF_DATA_PER_REQUEST = 50
    WINDOW_MINUTES = 15


def add_users_to_list(
        api: tweepy.API,
        list_id: str,
        user_ids: list[str],
        user_names: list[str] = [],
        add_only_users_with_diff: bool = False,
        num_of_data_per_request: int = EnumOfUserForList.MAX_NUM_OF_DATA_PER_REQUEST.value
    ) -> None:
    
    '''
    ユーザ(複数)追加
    
    Args:
        api (tweepy.API)                            : API
        list_id (str)                               : リストID
        user_ids (list[str])                        : ユーザID(複数)
        user_names (list[str])                      : ユーザ名(複数)
        add_only_users_with_diff (bool, optional)   : 差分ユーザ追加
        num_of_data_per_request (int, optional)     : リクエストごとのデータ数
    
    Returns:
        -
    
    Notes:
        - 認証
            - ユーザ認証(OAuth 1.0a)
        - エンドポイント
            - POST lists/members/create_all
        - レート制限
            - ユーザ認証(OAuth 1.0a)
                - データ数／リクエスト : 100
                - リクエスト数／１５分 : (未公表)
        - 指定したユーザを全て追加できるようにするため、以下のアカウントを除外する
            - 削除されたアカウント
            - 凍結されたアカウント
            - 保護されたアカウント
            - 自分をブロックしたアカウント
            - 自分がブロックしたアカウント
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/post-lists-members-create_all
        - レスポンス
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-show#example-response
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    # 認証方式の確認
    if isinstance(api.auth, (tweepy.OAuth1UserHandler)) == False:
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    # 引数の検証：ユーザ名の長さがユーザIDの長さと同じであること
    if len(user_names) > 0 \
        and len(user_ids) != len(user_names):
        raise(pyl.CustomError(
            f'ユーザ名(複数)の長さがユーザID(複数)の長さと異なります。' +
            f'(user_names:{len(user_names)}, user_ids:{len(user_ids)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        
        # ユーザ名の初期化
        if len(user_names) == 0:
            user_names = ['-'] * len(user_ids)
        
        # ユーザの分割(未追加、追加済み)
        users_of_unadded_and_added: tuple[list[str], list[str], list[str], list[str]] = \
            __split_users_into_unadded_and_added(
                    api,
                    add_only_users_with_diff,
                    list_id,
                    user_ids,
                    user_names
                )
        user_ids_of_unadded_account: list[str] = users_of_unadded_and_added[0]
        user_names_of_unadded_account: list[str] = users_of_unadded_and_added[1]
        user_ids_of_added_account: list[str] = users_of_unadded_and_added[2]
        num_of_users_of_added_account: int = len(user_ids_of_added_account)
        
        # ユーザの分割(問題なし、問題あり)
        users_with_no_problems_and_problems: tuple[list[str], list[str], list[str], list[str]] = \
            __split_users_into_no_problems_and_problems(
                    api,
                    user_ids_of_unadded_account,
                    user_names_of_unadded_account,
                    EnumOfUserForLookup.MAX_NUM_OF_DATA_PER_REQUEST.value
                )
        user_ids_without_problems: list[str] = users_with_no_problems_and_problems[0]
        user_ids_with_problems: list[str] = users_with_no_problems_and_problems[2]
        user_names_with_problems: list[str] = users_with_no_problems_and_problems[3]
        num_of_users_without_problems: int = len(user_ids_without_problems)
        num_of_users_with_problems: int = len(user_ids_with_problems)
        
        # ログの出力
        if add_only_users_with_diff == True:
            pyl.log_inf(lg, f'追加済みユーザを除外しました。' +
                            f'(num_of_users_of_added_account:{num_of_users_of_added_account})')
        pyl.log_inf(lg, f'下記ユーザは問題があるため除外しました。' +
                        f'(num_of_users_with_problems:{num_of_users_with_problems})')
        pyl.log_inf(lg, f'ユーザID：{user_ids_with_problems}')
        pyl.log_inf(lg, f'ユーザ名：{user_names_with_problems}')
        pyl.log_inf(lg, f'{num_of_data_per_request}人ごとにユーザを追加します。' +
                        f'(num_of_users_without_problems:{num_of_users_without_problems})')
        util.show_estimated_proc_time(
                num_of_users_without_problems,
                num_of_data_per_request,
                windows_minutes=EnumOfUserForList.WINDOW_MINUTES
            )
        
        # ユーザIDリスト
        user_ids_list: list[list[str]] = pyl.split_list(
            user_ids_without_problems, num_of_data_per_request)
        
        # ユーザIDリストの要素ごと
        user_ids_by_element: list[str]
        sum_of_users_at_this_time: int = num_of_users_of_added_account
        sum_of_users_at_last_time: int = 0
        num_of_users_at_this_time: int = 0
        for index, user_ids_by_element in enumerate(user_ids_list, start=1):
            # ユーザの追加
            sum_of_users_at_last_time = sum_of_users_at_this_time
            list_: Any = api.add_list_members(list_id=list_id, screen_name=user_ids_by_element)
            sum_of_users_at_this_time = list_.member_count
            num_of_users_at_this_time = sum_of_users_at_this_time - sum_of_users_at_last_time
            
            # ログの出力
            num_of_users_by_element: int = len(user_ids_by_element)
            pyl.log_inf(lg, f'ユーザを追加しました。' +
                            f'(num_of_users_at_this_time:' +
                            f'{num_of_users_at_this_time}/{num_of_users_by_element}, ' +
                            f'sum_of_users_at_this_time:' +
                            f'{sum_of_users_at_this_time - num_of_users_of_added_account}' +
                            f'/{num_of_users_without_problems})')
            
            # 追加結果の確認
            if num_of_users_at_this_time != num_of_users_by_element:
                raise(pyl.CustomError(f'HTTPステータスコードが正常(2xx)以外の可能性があります。'))
            
            # 待機
            if index != len(user_ids_list):
                datetime_dt: datetime = \
                    (datetime.now() + timedelta(minutes=EnumOfUserForList.WINDOW_MINUTES.value))
                datetime_str: str = datetime_dt.strftime('%Y-%m-%d %H:%M:%S')
                pyl.log_inf(lg, f'{EnumOfUserForList.WINDOW_MINUTES.value}分後' +
                                f'({datetime_str})に後続の処理を実行します。')
                time.sleep(60 * EnumOfUserForList.WINDOW_MINUTES.value)
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'ユーザ(複数)追加に失敗しました。')
        raise(e)
    
    return None


def __split_users_into_unadded_and_added(
        api: tweepy.API,
        add_only_users_with_diff: bool,
        list_id: str,
        user_ids: list[str],
        user_names: list[str]
    ) -> tuple[list[str], list[str], list[str], list[str]]:
    
    '''ユーザ分割(未追加、追加済み)'''
    
    lg: Optional[Logger] = None
    
    # ユーザID(未追加)
    user_ids_of_unadded_account: list[str] = []
    # ユーザ名(未追加)
    user_names_of_unadded_account: list[str] = []
    # ユーザID(追加済み)
    user_ids_of_added_account: list[str] = []
    # ユーザID(追加済みTEMP)
    user_ids_of_added_account_temp: list[str] = []
    # ユーザ名(追加済み)
    user_names_of_added_account: list[str] = []
    
    try:
        lg = pyl.get_logger(__name__)
        
        if add_only_users_with_diff == True:
            # ユーザID(追加済みアカウント)の生成
            list_member_pages: list[ResultSet] = get_list_member_pages(api, list_id)
            for list_members_by_page in list_member_pages:
                for list_member in list_members_by_page:
                    user_ids_of_added_account_temp.append(list_member.screen_name)
            
            # ユーザID・名(未追加・追加済みアカウント)の生成
            for index, user_id in enumerate(user_ids):
                if not(user_id in user_ids_of_added_account_temp):
                    user_ids_of_unadded_account.append(user_id)
                    user_names_of_unadded_account.append(user_names[index])
                else:
                    user_ids_of_added_account.append(user_id)
                    user_names_of_added_account.append(user_names[index])
            
            pyl.log_inf(lg, f'追加済みユーザの除外に成功しました。')
        else:
            user_ids_of_unadded_account = user_ids
            user_names_of_unadded_account = user_names
    except Exception as e:
        raise(e)
    
    return user_ids_of_unadded_account, \
            user_names_of_unadded_account, \
            user_ids_of_added_account, \
            user_names_of_added_account


def __split_users_into_no_problems_and_problems(
        api: tweepy.API,
        user_ids: list[str],
        user_names: list[str],
        num_of_data_per_request: int
    ) -> tuple[list[str], list[str], list[str], list[str]]:
    
    '''ユーザ分割(問題なし、問題あり)'''
    
    lg: Optional[Logger] = None
    
    # ユーザID(問題なし)
    user_ids_without_problems: list[str] = []
    # ユーザ名(問題なし)
    user_names_without_problems: list[str] = []
    # ユーザID(問題あり)
    user_ids_with_problems: list[str] = []
    # ユーザ名(問題あり)
    user_names_with_problems: list[str] = []
    
    try:
        lg = pyl.get_logger(__name__)
        
        # ユーザID(未削除・未凍結・未保護アカウント)の生成
        user_ids_of_unprotected_account: list[str] = []
        user_pages: list[ResultSet] = lookup_users(api, user_ids, num_of_data_per_request)
        for users_by_page in user_pages:
            for user in users_by_page:
                if user.protected == False:
                    user_ids_of_unprotected_account.append(user.screen_name)
        
        pyl.log_inf(lg, f'削除されたアカウント、凍結されたアカウント、保護されたアカウントの除外に成功しました。')
        pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
        
        # ユーザID(未ブロックアカウント)の生成
        user_ids_of_accounts_that_has_not_blocked_me: list[str] = []
        auth_user_info : Any = get_auth_user_info(api)
        for user_id in user_ids_of_unprotected_account:
            friendship: Any = get_friendship(api, user_id, auth_user_info.screen_name)
            if friendship[0].blocking is None or friendship[0].blocking == False:
                user_ids_of_accounts_that_has_not_blocked_me.append(user_id)
        
        pyl.log_inf(lg, f'自分をブロックしたアカウントの除外に成功しました。')
        
        # ユーザID(ブロック済みアカウント)の生成
        user_ids_of_accounts_that_i_have_blocked: list[str] = []
        blocked_user_pages: list[ResultSet] = get_blocked_users_pages(api)
        for blocked_users_by_page in blocked_user_pages:
            for blocked_user in blocked_users_by_page:
                user_ids_of_accounts_that_i_have_blocked.append(blocked_user.screen_name)
        
        # ユーザID(未ブロックアカウント)の生成
        user_ids_of_accounts_that_i_have_not_blocked: list[str] = []
        for user_id in user_ids_of_accounts_that_has_not_blocked_me:
            if not(user_id in user_ids_of_accounts_that_i_have_blocked):
                user_ids_of_accounts_that_i_have_not_blocked.append(user_id)
        
        pyl.log_inf(lg, f'自分がブロックしたアカウントの除外に成功しました。')
        
        # ユーザID・名(問題なし・あり)の生成
        for index, user_id in enumerate(user_ids):
            if not(user_id in user_ids_of_accounts_that_i_have_not_blocked):
                user_ids_with_problems.append(user_id)
                user_names_with_problems.append(user_names[index])
            else:
                user_ids_without_problems.append(user_id)
                user_names_without_problems.append(user_names[index])
        
        pyl.log_inf(lg, f'ユーザの分割に成功しました。')
    except Exception as e:
        raise(e)
    
    return user_ids_without_problems, \
            user_names_without_problems, \
            user_ids_with_problems, \
            user_names_with_problems


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
    if isinstance(api.auth, (tweepy.OAuth1UserHandler)) == False:
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        
        # 認証ユーザ情報の取得
        auth_user_info : Any = api.verify_credentials()
        
        pyl.log_inf(lg, f'認証ユーザ情報取得に成功しました。' +
                        f'(user_id:{auth_user_info.screen_name: <15}, ' +
                        f'user_name:{auth_user_info.name})')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'認証ユーザ情報取得に失敗しました。')
        raise(e)
    
    return auth_user_info


####################################################################################################
# Mute, block, and report users
####################################################################################################


class EnumOfBlockedUser():
    class EnumOfOauth1User(IntEnum):
        MAX_NUM_OF_DATA_PER_REQUEST = 5000
        MAX_NUM_OF_REQUESTS_PER_15MIN = 15
        MAX_NUM_OF_DATA_PER_15MIN = MAX_NUM_OF_DATA_PER_REQUEST * MAX_NUM_OF_REQUESTS_PER_15MIN


def get_blocked_users_pages(
        api: tweepy.API,
        num_of_data: int =
        EnumOfBlockedUser.EnumOfOauth1User.MAX_NUM_OF_DATA_PER_15MIN.value,
        num_of_data_per_request: int =
        EnumOfBlockedUser.EnumOfOauth1User.MAX_NUM_OF_DATA_PER_REQUEST.value
    ) -> list[ResultSet]:
    
    '''
    ブロックユーザページの取得
    
    Args:
        api (tweepy.API)                        : API
        num_of_data (int, optional)             : データ数
        num_of_data_per_request (int, optional) : リクエストごとのデータ数
    
    Returns:
        list[ResultSet] : ブロックユーザページ (list[ResultSet[tweepy.models.User]])
    
    Notes:
        - 認証
            - ユーザ認証(OAuth 1.0a)
        - エンドポイント
            - GET blocks/list
        - レート制限
            - ユーザ認証(OAuth 1.0a)
                - データ数／リクエスト : 5000
                - リクエスト数／１５分 : 15
                    - 超過した場合は15分の待機時間が発生する
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/mute-block-report-users/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/mute-block-report-users/api-reference/get-blocks-list
        - レスポンス
            - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    blocked_user_pages: list[ResultSet] = []
    
    # 認証方式の確認
    if isinstance(api.auth, (tweepy.OAuth1UserHandler)) == False:
        raise(pyl.CustomError(
            f'この認証方式ではTwitterAPIにアクセスできません。(Auth:{type(api.auth)})'))
    
    try:
        lg = pyl.get_logger(__name__)
        # pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
        
        # リクエスト数の算出
        num_of_requests = math.ceil(num_of_data / num_of_data_per_request)
        
        # ブロックユーザページの取得
        blocked_user_pagination: tweepy.Cursor = tweepy.Cursor(
                api.get_blocks,
            )
        blocked_user_pages = list(blocked_user_pagination.pages(num_of_requests))
        
        pyl.log_inf(lg, f'ブロックユーザページ取得に成功しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_err(lg, f'ブロックユーザページ取得に失敗しました。')
        raise(e)
    
    return blocked_user_pages

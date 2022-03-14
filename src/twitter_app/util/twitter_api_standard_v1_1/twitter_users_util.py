from enum import IntEnum
from logging import Logger
from typing import Any, Optional

import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet

####################################################################################################
# Follow, search, and get users
####################################################################################################


class Followee(IntEnum):
    MAX_NUM_OF_DATA_PER_REQUEST = 200
    MAX_NUM_OF_REQUESTS_PER_15MIN = 15


def get_followee_pages(
        api: tweepy.API,
        user_id: str,
        num_of_data_per_request: int = Followee.MAX_NUM_OF_DATA_PER_REQUEST.value,
        num_of_requests: int = Followee.MAX_NUM_OF_REQUESTS_PER_15MIN.value
    ) -> list[ResultSet]:
    
    '''
    フォロイーページ取得
    
    Args:
        api (tweepy.API)                : API
        user_id (str)                   : ユーザID
        num_of_data_per_request (int)   : リクエストごとのデータ数(デフォルト：200)
        num_of_requests (int)           : リクエスト数(デフォルト：15)
    
    Returns:
        list[ResultSet] : フォロイーページ (list[ResultSet[tweepy.models.User]])
    
    Notes:
        - 使用するエンドポイントはGETメソッドである
        - 引数「リクエストごとのデータ数」は上限が200データ
            - 超過して指定した場合は200で上書きする
        - 引数「リクエスト数」は15分ごとに最大15リクエスト
            - 超過して指定した場合はレート制限により15分の待機時間が発生する
        - 15分で最大3000データを取得できる
            - 200 data/req * 15 req/15-min = 3000 data/15-min
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-friends-list
        - オブジェクトモデル
            - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    followee_pages: list[ResultSet] = []
    
    try:
        lg = pyl.get_logger(__name__)
        
        pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
        
        followee_pagination: tweepy.Cursor = tweepy.Cursor(
                api.get_friends,
                screen_name=user_id,
                count=num_of_data_per_request
                if num_of_data_per_request <= Followee.MAX_NUM_OF_DATA_PER_REQUEST.value
                else Followee.MAX_NUM_OF_DATA_PER_REQUEST.value
            )
        followee_pages = list(followee_pagination.pages(num_of_requests))
        
        pyl.log_inf(lg, f'フォロイーページ取得に成功しました。')
    except Exception as e:
        if lg is not None:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_war(lg, f'フォロイーページ取得に失敗しました。' +
                            f'(user_id:{user_id}, err_msg:{err_msg})')
    
    return followee_pages


class Follower(IntEnum):
    MAX_NUM_OF_DATA_PER_REQUEST = 200
    MAX_NUM_OF_REQUESTS_PER_15MIN = 15


def get_follower_pages(
        api: tweepy.API,
        user_id: str,
        num_of_data_per_request: int = Follower.MAX_NUM_OF_DATA_PER_REQUEST.value,
        num_of_requests: int = Follower.MAX_NUM_OF_REQUESTS_PER_15MIN.value
    ) -> list[ResultSet]:
    
    '''
    フォロワーページ取得
    
    Args:
        api (tweepy.API)                : API
        user_id (str)                   : ユーザID
        num_of_data_per_request (int)   : リクエストごとのデータ数(デフォルト：200)
        num_of_requests (int)           : リクエスト数(デフォルト：15)
    
    Returns:
        list[ResultSet] : フォロワーページ (list[ResultSet[tweepy.models.User]])
    
    Notes:
        - 「フォロイーページ取得」を参照する
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-followers-list
        - オブジェクトモデル
            - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    follower_pages: list[ResultSet] = []
    
    try:
        lg = pyl.get_logger(__name__)
        
        pyl.log_inf(lg, f'時間がかかるため気長にお待ちください。')
        
        follower_pagination: tweepy.Cursor = tweepy.Cursor(
                api.get_followers,
                screen_name=user_id,
                count=num_of_data_per_request
                if num_of_data_per_request <= Follower.MAX_NUM_OF_DATA_PER_REQUEST.value
                else Follower.MAX_NUM_OF_DATA_PER_REQUEST.value
            )
        follower_pages = list(follower_pagination.pages(num_of_requests))
        
        pyl.log_inf(lg, f'フォロワーページ取得に成功しました。')
    except Exception as e:
        if lg is not None:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_war(lg, f'フォロワーページ取得に失敗しました。' +
                            f'(user_id:{user_id}, err_msg:{err_msg})')
    
    return follower_pages


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
        - 使用するエンドポイントはGETメソッドである
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-users-show
        - オブジェクトモデル
            - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
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


def has_twitter_list(
        api: tweepy.API,
        twitter_list_name: str
    ) -> bool:
    
    '''
    Twitterリスト存在有無確認
    
    Args:
        api (tweepy.API)        : API
        twitter_list_name (str) : Twitterリスト名
    
    Returns:
        bool: Twitterリスト存在有無 (True：有、False：無)
    
    Notes:
        - 使用するエンドポイントはGETメソッドである
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-list
        - オブジェクトモデル
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-show#example-response
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    has_twitter_list: bool = False
    
    try:
        lg = pyl.get_logger(__name__)
        
        twitter_lists: Any = api.get_lists(reverse=True)
        
        for twitter_list in twitter_lists:
            if twitter_list.name == twitter_list_name:
                pyl.log_inf(lg, f'Twitterリストが既に存在します。' +
                                f'(twitter_list_name:{twitter_list_name})')
                has_twitter_list = True
                break
    except Exception as e:
        if lg is not None:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_war(lg, f'Twitterリスト存在有無確認に失敗しました。' +
                            f'(twitter_list_name:{twitter_list_name}, err_msg:{err_msg})')
    
    return has_twitter_list


def get_twitter_lists(
        api: tweepy.API,
        user_id: str = ''
    ) -> ResultSet:
    
    '''
    Twitterリスト一覧取得
    
    Args:
        api (tweepy.API)    : API
        user_id (str)       : ユーザID
    
    Returns:
        ResultSet: Twitterリスト一覧 (ResultSet[tweepy.models.List])
    
    Notes:
        - 使用するエンドポイントはGETメソッドである
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-list
        - オブジェクトモデル
            - https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/lists
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-show#example-response
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        twitter_lists: Any
        if user_id == '':
            twitter_lists = api.get_lists(reverse=True)
        else:
            twitter_lists = api.get_lists(screen_name=user_id, reverse=True)
        
        pyl.log_inf(lg, f'Twitterリスト一覧取得に成功しました。(user_id:{user_id})')
    except Exception as e:
        if lg is not None:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_err(lg, f'Twitterリスト一覧取得に失敗しました。' +
                            f'(user_id:{user_id}, err_msg:{err_msg})')
        raise(e)
    
    return twitter_lists


class ListMember(IntEnum):
    MAX_NUM_OF_DATA_PER_REQUEST = 5000
    MAX_NUM_OF_REQUESTS_PER_15MIN = 900


def get_twitter_list_member_pages(
        api: tweepy.API,
        twitter_list_id: str,
        num_of_data_per_request: int = ListMember.MAX_NUM_OF_DATA_PER_REQUEST.value,
        num_of_requests: int = ListMember.MAX_NUM_OF_REQUESTS_PER_15MIN.value
    ) -> list[ResultSet]:
    
    '''
    Twitterリストメンバーページ取得
    
    Args:
        api (tweepy.API)                : API
        twitter_list_id (str)           : TwitterリストID
        num_of_data_per_request (int)   : リクエストごとのデータ数(デフォルト：5000)
        num_of_requests (int)           : リクエスト数(デフォルト：900)
    
    Returns:
        list[ResultSet] : Twitterリストメンバーページ (list[ResultSet[tweepy.models.User]])
    
    Notes:
        - 使用するエンドポイントはGETメソッドである
        - 引数「リクエストごとのデータ数」は上限が5000データ
            - 超過して指定した場合は5000で上書きする
        - 引数「リクエスト数」は15分ごとに最大900リクエスト
            - 超過して指定した場合はレート制限により15分の待機時間が発生する
        - 15分で最大450万データを取得できる
            - 5000 data/req * 900 req/15-min = 4,500,000 data/15-min
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-members
        - オブジェクトモデル
            - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    list_member_pages: list[ResultSet] = []
    
    try:
        lg = pyl.get_logger(__name__)
        
        list_member_pagination: tweepy.Cursor = tweepy.Cursor(
                api.get_list_members,
                list_id=twitter_list_id,
                count=num_of_data_per_request
                if num_of_data_per_request <= ListMember.MAX_NUM_OF_DATA_PER_REQUEST.value
                else ListMember.MAX_NUM_OF_DATA_PER_REQUEST.value
            )
        list_member_pages = list(list_member_pagination.pages(num_of_requests))
        
        pyl.log_inf(lg, f'Twitterリストメンバーページ取得に成功しました。' +
                        f'(twitter_list_id:{twitter_list_id})')
    except Exception as e:
        if lg is not None:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_war(lg, f'Twitterリストメンバーページ取得に失敗しました。' +
                            f'(twitter_list_id:{twitter_list_id}, err_msg:{err_msg})')
    
    return list_member_pages


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
        - 使用するエンドポイントはPOSTメソッドである
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/post-lists-create
        - オブジェクトモデル
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-show#example-response
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        twitter_list: Any = api.create_list(twitter_list_name, mode='private', description='')
        
        pyl.log_inf(lg, f'Twitterリスト生成に成功しました。(twitter_list_name:{twitter_list_name})')
    except Exception as e:
        if lg is not None:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_err(lg, f'Twitterリスト生成に失敗しました。' +
                            f'(twitter_list_name:{twitter_list_name}, err_msg:{err_msg})')
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
        - 使用するエンドポイントはPOSTメソッドである
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/post-lists-destroy
        - オブジェクトモデル
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-show#example-response
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    result: bool = False
    
    try:
        lg = pyl.get_logger(__name__)
        
        twitter_lists: Any = api.get_lists(reverse=True)
        
        for twitter_list in twitter_lists:
            if twitter_list.name == twitter_list_name:
                api.destroy_list(list_id=twitter_list.id)
                pyl.log_inf(lg, f'Twitterリスト破棄に成功しました。' +
                                f'(twitter_list_name:{twitter_list_name})')
                result = True
                break
    except Exception as e:
        if lg is not None:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_war(lg, f'Twitterリスト破棄に失敗しました。' +
                            f'(twitter_list_name:{twitter_list_name}, err_msg:{err_msg})')
    
    return result


def add_user_to_twitter_list(
        api: tweepy.API,
        twitter_list_id: str,
        user_id: str,
        user_name: str = ''
    ) -> bool:
    
    '''
    ユーザ追加
    
    Args:
        api (tweepy.API)            : API
        twitter_list_id (str)       : TwitterリストID
        user_id (str)               : ユーザID
        user_name (str, optional)   : ユーザ名
    
    Returns:
        bool: 実行結果 (True：成功、False：失敗)
    
    Notes:
        - 使用するエンドポイントはPOSTメソッドである
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/post-lists-members-create
        - オブジェクトモデル
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-show#example-response
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    result: bool = False
    
    try:
        lg = pyl.get_logger(__name__)
        
        api.add_list_member(list_id=twitter_list_id, screen_name=user_id)
        pyl.log_deb(lg, f'ユーザ追加に成功しました。(user_id:{user_id: <15}, user_name:{user_name})')
        
        result = True
    except Exception as e:
        if lg is not None:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_war(lg, f'ユーザ追加に失敗しました。鍵付きや削除済みの可能性があります。' +
                            f'(user_id:{user_id: <15}, user_name:{user_name}, err_msg:{err_msg})')
    
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
        - 使用するエンドポイントはGETメソッドである
    
    References:
        - エンドポイント
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/manage-account-settings/overview
            - https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/manage-account-settings/api-reference/get-account-verify_credentials
        - オブジェクトモデル
            - https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
    '''  # noqa: E501
    
    lg: Optional[Logger] = None
    
    try:
        lg = pyl.get_logger(__name__)
        
        auth_user_info : Any = api.verify_credentials()
        
        pyl.log_inf(lg, f'認証ユーザ情報取得に成功しました。' +
                        f'(user_id:{auth_user_info.screen_name: <15}, ' +
                        f'user_name:{auth_user_info.name})')
    except Exception as e:
        if lg is not None:
            err_msg: str = str(e).replace('\n', ' ')
            pyl.log_err(lg, f'認証ユーザ情報取得に失敗しました。')
        raise(e)
    
    return auth_user_info

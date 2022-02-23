from logging import Logger
from typing import Any, Optional

import python_lib_for_me as mylib
import tweepy


def has_twitter_list(api: tweepy.API, twitter_list_name: str) -> bool:
    '''Twitterリスト存在有無確認'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = mylib.get_logger(__name__)
        
        twitter_lists: Any = api.get_lists()
        
        for twitter_list in twitter_lists:
            if twitter_list.name == twitter_list_name:
                lg.info(f'Twitterリストが既に存在します。(twitter_list_name:{twitter_list_name})')
                return True
    except Exception as e:
        raise(e)
    
    return False


def generate_twitter_list(api: tweepy.API, twitter_list_name: str) -> tweepy.List:
    '''Twitterリスト生成'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = mylib.get_logger(__name__)
        
        twitter_list: Any = api.create_list(twitter_list_name, mode='private', description='')
        lg.info(f'Twitterリスト生成に成功しました。(twitter_list_name:{twitter_list_name})')
    except Exception as e:
        if lg is not None:
            lg.warning(f'Twitterリスト生成に失敗しました。(twitter_list_name:{twitter_list_name})')
        raise(e)
    
    return twitter_list


def destroy_twitter_list(api: tweepy.API, twitter_list: tweepy.List) -> None:
    '''Twitterリスト破棄'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = mylib.get_logger(__name__)
        
        api.destroy_list(list_id=twitter_list.id)
        lg.info(f'Twitterリスト破棄に成功しました。(twitter_list:{twitter_list.name})')
    except Exception as e:
        if lg is not None:
            lg.warning(f'Twitterリスト破棄に失敗しました。(twitter_list:{twitter_list.name})')
        raise(e)
    
    return None


def add_user(api: tweepy.API, twitter_list: tweepy.List, user_id: str, user_name: str) -> bool:
    '''ユーザ追加'''
    
    lg: Optional[Logger] = None
    
    try:
        lg = mylib.get_logger(__name__)
        
        api.add_list_member(list_id=twitter_list.id, screen_name=user_id)
        lg.debug(f'ユーザ追加に成功しました。(user_id:{user_id: <15}, user_name:{user_name})')
    except Exception as e:
        if lg is not None:
            lg.warning(f'ユーザ追加に失敗しました。鍵付きや削除済みの可能性があります。' +
                        f'(user_id:{user_id: <15}, user_name:{user_name})')
        return False
    
    return True

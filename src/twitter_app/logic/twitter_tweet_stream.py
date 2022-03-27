from enum import IntEnum, auto
from logging import Logger
from typing import Any, Optional

import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet

from twitter_app.util.twitter_api_v1_1.standard import twitter_tweets_util, twitter_users_util


class EnumOfItemProcTarget(IntEnum):
    USER_ID = auto()
    LIST_ID = auto()
    LIST_NAME = auto()


def do_logic(
        api: tweepy.API,
        enum_of_item_proc_target: EnumOfItemProcTarget,
        item: str,
        keyword_of_csv_format: str,
    ) -> None:
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'Twitterツイート配信を開始します。')
        
        # ユーザページの取得
        user_pages: list[ResultSet] = []
        if enum_of_item_proc_target == EnumOfItemProcTarget.USER_ID:
            # 指定したユーザIDのフォロイーのツイートを配信する場合
            user_pages = twitter_users_util.get_followee_pages(
                    api,
                    user_id=item,
                    num_of_data=twitter_tweets_util.EnumOfStream.MAX_NUM_OF_FOLLOWING.value
                )
        elif enum_of_item_proc_target == EnumOfItemProcTarget.LIST_ID:
            # 指定したリストIDのツイートを配信する場合
            user_pages = twitter_users_util.get_list_member_pages(api, list_id=item)
        elif enum_of_item_proc_target == EnumOfItemProcTarget.LIST_NAME:
            # 指定したリスト名のツイートを配信する場合
            can_stream_by_list_name: bool = False
            lists: ResultSet = twitter_users_util.get_lists(api)
            for list_ in lists:
                if list_.name == item:
                    user_pages = twitter_users_util.get_list_member_pages(api, list_id=list_.id)
                    can_stream_by_list_name = True
                    break
            if can_stream_by_list_name == False:
                raise(pyl.CustomError(f'リスト取得に失敗しました。(list_name:{item})'))
        
        # フォローユーザIDの生成
        following_user_ids: list[str] = [
            user.id
            for users_by_page in user_pages
            for user in users_by_page]
        auth_user_info : Any = twitter_users_util.get_auth_user_info(api)
        following_user_ids.append(auth_user_info.id)
        
        # キーワードリストの生成
        keywords: list[str] = pyl.generate_str_list_from_csv(keyword_of_csv_format)
        
        # ツイートの配信
        twitter_tweets_util.stream_tweets(api, following_user_ids, keywords)
        
        pyl.log_inf(lg, f'Twitterツイート配信を終了します。')
    except Exception as e:
        raise(e)
    
    return None

from logging import Logger
from typing import Any, Optional

import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet

from twitter_app.util.twitter_api_v1_1.standard import twitter_tweets_util, twitter_users_util


def do_logic(
        api: tweepy.API,
        id: str,
        keyword_of_csv_format: str,
        stream_by_list_id: bool = False
    ) -> None:
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f'Twitterツイート配信を開始します。')
        
        # ユーザページの取得
        user_pages: list[ResultSet]
        if stream_by_list_id == False:
            # 指定したユーザIDのフォロイーのツイートを配信する場合
            user_pages = twitter_users_util.get_followee_pages(
                    api,
                    user_id=id,
                    num_of_data=twitter_tweets_util.EnumOfStream.MAX_NUM_OF_FOLLOWING.value
                )
        else:
            # 指定したリストIDのツイートを配信する場合
            user_pages = twitter_users_util.get_list_member_pages(api, list_id=id)
        
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

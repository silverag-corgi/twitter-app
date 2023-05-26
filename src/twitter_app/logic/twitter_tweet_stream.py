from enum import IntEnum, auto
from logging import Logger
from typing import Optional

import pandas as pd
import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet

from twitter_app.util import const_util, pandas_util
from twitter_app.util.twitter_api_v1_1.standard import twitter_tweets_util, twitter_users_util


class EnumOfProcTargetItem(IntEnum):
    USER_ID = auto()
    LIST_ID = auto()
    LIST_NAME = auto()
    FILE_PATH = auto()


def do_logic(
    api: tweepy.API,
    enum_of_proc_target_item: EnumOfProcTargetItem,
    item: str,
    keyword_of_csv_format: str,
    header_line_num: int = -1,
) -> None:
    lg: Optional[Logger] = None

    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f"Twitterツイート配信を開始します。")

        # ユーザページの取得
        user_pages: list[ResultSet] = []
        if enum_of_proc_target_item == EnumOfProcTargetItem.USER_ID:
            # 指定したユーザIDのフォロイーのツイートを配信する場合
            user_pages = twitter_users_util.get_followee_pages(
                api,
                user_id=item,
                num_of_data=twitter_tweets_util.EnumOfStream.MAX_NUM_OF_FOLLOWING.value,
            )
        elif enum_of_proc_target_item == EnumOfProcTargetItem.LIST_ID:
            # 指定したリストIDのツイートを配信する場合
            user_pages = twitter_users_util.get_list_member_pages(api, list_id=item)
        elif enum_of_proc_target_item == EnumOfProcTargetItem.LIST_NAME:
            # 指定したリスト名のツイートを配信する場合
            lists: ResultSet = twitter_users_util.get_lists(api)
            for list_ in lists:
                if list_.name == item:
                    user_pages = twitter_users_util.get_list_member_pages(api, list_id=list_.id)
                    break
        elif enum_of_proc_target_item == EnumOfProcTargetItem.FILE_PATH:
            # 指定したファイルに記載されているユーザのツイートを配信する場合
            list_member_df: pd.DataFrame = pandas_util.read_list_member_file(item, header_line_num)
            user_ids: list[str] = [
                str(list_member[const_util.LIST_MEMBER_HEADER[0]])
                for _, list_member in list_member_df.iterrows()
            ]
            user_pages = twitter_users_util.lookup_users(api, user_ids)

        # フォローユーザIDの生成
        following_user_ids: list[str] = [
            user.id for users_by_page in user_pages for user in users_by_page
        ]
        if len(following_user_ids) > 0:
            pyl.log_inf(lg, f"配信対象：{len(following_user_ids)}人")
        else:
            raise (pyl.CustomError(f"フォローユーザが存在しません。"))

        # キーワードリストの生成
        keywords: list[str] = pyl.generate_str_list_from_csv(keyword_of_csv_format)

        # ツイートの配信
        twitter_tweets_util.stream_tweets(api, following_user_ids, keywords)
    except Exception as e:
        raise (e)
    finally:
        pyl.log_inf(lg, f"Twitterツイート配信を終了します。")

    return None

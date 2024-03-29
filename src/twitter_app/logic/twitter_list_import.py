import glob
import os
from typing import Any, Optional

import pandas as pd
import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet

from twitter_app.util import const_util, pandas_util
from twitter_app.util.twitter_api_v1_1.standard import twitter_users_util


def do_logic(
    use_debug_mode: bool,
    api: tweepy.API,
    list_member_file_path_with_wildcard: str,
    header_line_num: int,
    add_only_users_with_diff: bool,
) -> None:
    """ロジック実行"""

    clg: Optional[pyl.CustomLogger] = None
    list_: Any = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__, use_debug_mode=use_debug_mode)
        clg.log_inf(f"ロジック実行(Twitterリストインポート)を開始します。")

        # リストメンバーファイルパスの取得
        list_member_file_paths: list[str] = glob.glob(list_member_file_path_with_wildcard)

        # リストメンバーファイルの件数が0件の場合
        if len(list_member_file_paths) == 0:
            clg.log_wrn(f"リストメンバーファイルの件数が0件です。(list_member_file_path:{list_member_file_path_with_wildcard})")
        else:
            # TwitterAPIの実行
            for list_member_file_path in list_member_file_paths:
                # リスト名の生成
                list_name: str = os.path.splitext(os.path.basename(list_member_file_path))[0]

                # 既存リストの取得
                if add_only_users_with_diff is True:
                    existing_lists: ResultSet = twitter_users_util.get_lists(use_debug_mode, api)
                    for existing_list in existing_lists:
                        if existing_list.name == list_name:
                            list_ = existing_list
                            break

                # リストの生成
                if add_only_users_with_diff is True and list_ is None:
                    list_ = twitter_users_util.generate_list(use_debug_mode, api, list_name)
                elif add_only_users_with_diff is False:
                    twitter_users_util.destroy_list(use_debug_mode, api, list_name)
                    list_ = twitter_users_util.generate_list(use_debug_mode, api, list_name)

                # リストメンバーデータフレームの取得(リストメンバーファイルの読み込み)
                list_member_df: pd.DataFrame = pandas_util.read_list_member_file(
                    use_debug_mode, list_member_file_path, header_line_num
                )

                # ユーザの追加
                twitter_users_util.add_users_to_list(
                    use_debug_mode,
                    api,
                    list_,
                    [
                        str(list_member[const_util.LIST_MEMBER_HEADER[0]]).strip()
                        for _, list_member in list_member_df.iterrows()
                    ],
                    [
                        str(list_member[const_util.LIST_MEMBER_HEADER[1]])
                        for _, list_member in list_member_df.iterrows()
                    ],
                    add_only_users_with_diff,
                )
    except Exception as e:
        # リストの破棄
        if list_ is not None:
            twitter_users_util.destroy_list(use_debug_mode, api, list_.name)

        raise (e)
    finally:
        if clg is not None:
            clg.log_inf(f"ロジック実行(Twitterリストインポート)を終了します。")

    return None

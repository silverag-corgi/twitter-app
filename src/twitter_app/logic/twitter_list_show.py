from enum import IntEnum, auto
from logging import Logger
from typing import Optional

import pandas as pd
import python_lib_for_me as pyl
import tweepy
from tweepy.models import ResultSet

from twitter_app.util import const_util
from twitter_app.util.twitter_api_v1_1.standard import twitter_users_util


class EnumOfProcTargetList(IntEnum):
    ALL = auto()
    ID = auto()
    NAME = auto()


def do_logic(
    api: tweepy.API,
    enum_of_proc_target_list: EnumOfProcTargetList,
    list_id_or_name_of_csv_format: str,
) -> pd.DataFrame:
    """
    ロジック実行

    Args:
        api (tweepy.API)                                : API
        enum_of_list_proc_target (EnumOfListProcTarget) : リスト処理対象
        list_id_or_name_of_csv_format (str)             : リストID(名前)(csv形式)

    Returns:
        pd.DataFrame: リストデータフレーム
    """

    lg: Optional[Logger] = None

    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        pyl.log_inf(lg, f"Twitterリスト表示を開始します。")

        # Pandasオプション設定
        pd.set_option("display.unicode.east_asian_width", True)

        # リスト(複数)の取得
        lists: ResultSet = twitter_users_util.get_lists(api)

        # リストデータフレームの初期化
        list_df: pd.DataFrame = pd.DataFrame(columns=const_util.LIST_HEADER)

        # リストデータフレームへの格納
        for list_ in lists:
            # リスト情報の取得
            creation_datetime: str = pyl.convert_timestamp_to_jst(str(list_.created_at))
            list_id_by_api: str = list_.id_str
            list_name_by_api: str = list_.name
            num_of_members: int = list_.member_count

            # リスト情報の格納(リスト処理対象ごと)
            list_info_df: pd.DataFrame
            if enum_of_proc_target_list == EnumOfProcTargetList.ALL:
                list_info_df = pd.DataFrame(
                    [[creation_datetime, list_id_by_api, list_name_by_api, num_of_members]],
                    columns=const_util.LIST_HEADER,
                )
                list_df = pd.concat([list_df, list_info_df], ignore_index=True)
            elif enum_of_proc_target_list == EnumOfProcTargetList.ID:
                # リストID(複数)(引数から)の生成
                list_ids_by_arg: list[str] = pyl.generate_str_list_from_csv(
                    list_id_or_name_of_csv_format
                )

                # リストID(APIから)がリストID(複数)(引数から)に存在する場合
                if list_id_by_api in list_ids_by_arg:
                    list_info_df = pd.DataFrame(
                        [[creation_datetime, list_id_by_api, list_name_by_api, num_of_members]],
                        columns=const_util.LIST_HEADER,
                    )
                    list_df = pd.concat([list_df, list_info_df], ignore_index=True)
            elif enum_of_proc_target_list == EnumOfProcTargetList.NAME:
                # リスト名(複数)(引数から)の生成
                list_names_by_arg: list[str] = pyl.generate_str_list_from_csv(
                    list_id_or_name_of_csv_format
                )

                # リスト名(引数から)がリスト名(APIから)に部分一致する場合
                for list_name_by_arg in list_names_by_arg:
                    if list_name_by_arg in list_name_by_api:
                        list_info_df = pd.DataFrame(
                            [[creation_datetime, list_id_by_api, list_name_by_api, num_of_members]],
                            columns=const_util.LIST_HEADER,
                        )
                        list_df = pd.concat([list_df, list_info_df], ignore_index=True)

        # リストデータフレームの表示
        pyl.log_inf(lg, f"リスト：\n{list_df}")
    except Exception as e:
        raise (e)
    finally:
        pyl.log_inf(lg, f"Twitterリスト表示を終了します。")

    return list_df

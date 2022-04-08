import pandas as pd

from twitter_app.util import const_util


def save_list_member_df(
        list_member_df: pd.DataFrame,
        list_member_file_path: str
    ) -> None:
    
    '''リストメンバーデータフレーム保存'''
    
    list_member_df.to_csv(
            list_member_file_path,
            header=True,
            index=False,
            mode='w',
            encoding=const_util.ENCODING
        )
    
    return None


def read_list_member_file(
        list_member_file_path: str,
        header_line_num: int
    ) -> pd.DataFrame:
    
    '''リストメンバーファイル読み込み'''
    
    list_member_df: pd.DataFrame = pd.read_csv(
            list_member_file_path,
            header=None,
            names=const_util.LIST_MEMBER_HEADER[0:2],
            index_col=None,
            usecols=[0, 1],
            skiprows=header_line_num,
            encoding=const_util.ENCODING
        )
    
    return list_member_df


def save_tweet_search_result_df(
        tweet_search_result_df: pd.DataFrame,
        tweet_search_result_file_path: str
    ) -> None:
    
    '''ツイート検索結果データフレーム保存'''
    
    tweet_search_result_df.to_csv(
            tweet_search_result_file_path,
            header=True,
            index=False,
            mode='w',
            encoding=const_util.ENCODING
        )
    
    return None

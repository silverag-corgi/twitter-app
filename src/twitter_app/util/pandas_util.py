import pandas as pd

from twitter_app.util import const_util


def save_twitter_list_df(
        twitter_list_df: pd.DataFrame,
        twitter_list_file_path: str
    ) -> None:
    
    '''Twitterリストデータフレーム保存'''
    
    twitter_list_df.to_csv(
            twitter_list_file_path,
            header=True,
            index=False,
            mode='w',
            encoding=const_util.ENCODING
        )
    
    return None


def read_twitter_list_file(
        twitter_list_csv_file_path: str,
        header_line_num: int
    ) -> pd.DataFrame:
    
    '''TwitterリストCSVファイル読み込み'''
    
    twitter_list_df: pd.DataFrame = pd.read_csv(
            twitter_list_csv_file_path,
            header=None,
            names=const_util.TWITTER_LIST_FILE_HEADER,
            index_col=None,
            usecols=[0, 1],
            skiprows=header_line_num,
            encoding=const_util.ENCODING
        )
    
    return twitter_list_df


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

import pandas as pd

from twitter_app.util import const_util


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

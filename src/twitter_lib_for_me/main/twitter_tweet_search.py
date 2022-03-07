import argparse
import os
import sys
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_lib_for_me.logic import twitter_api_auth, twitter_tweet_search


def main() -> int:
    
    '''
    メイン
    
    Summary:
        コマンドラインから実行する。
        
        引数を検証して問題ない場合、指定したクエリでツイートを検索し、ツイート検索結果ファイルを生成する。
    
    Args:
        -
    
    Args on cmd line:
        query (str)             : [必須] クエリ
        num_of_tweets (int)     : [任意] ツイート数(デフォルト：18000)
    
    Returns:
        int: 終了コード(0：正常、1：異常)
    
    Destinations:
        ツイート検索結果ファイル: ./dest/tweet_search_result/tweet_search_result_[クエリ].csv
    '''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = pyl.get_logger(__name__)
        
        # 実行コマンド表示
        sys.argv[0] = os.path.basename(sys.argv[0])
        pyl.log_inf(lg, f'実行コマンド：{sys.argv}')
        
        # 引数取得＆検証
        args: argparse.Namespace = __get_args()
        if __validate_args(args) == False:
            return 1
        
        # TwitterAPI認証ロジックの実行
        api: tweepy.API = twitter_api_auth.do_logic_of_api_by_oauth_1_user()
        
        # Twitterツイート検索ロジックの実行
        twitter_tweet_search.do_logic(api, args.query, args.num_of_tweets)
    except Exception as e:
        if lg is not None:
            pyl.log_exc(lg, '')
        return 1
    
    return 0


def __get_args() -> argparse.Namespace:
    '''引数取得'''
    
    try:
        parser: argparse.ArgumentParser = argparse.ArgumentParser(
                formatter_class=argparse.RawTextHelpFormatter,
                exit_on_error=True
            )
        
        help_msg: str = ''
        
        # 必須の引数
        help_msg =  'クエリ\n' + \
                    'RTと返信はデフォルトで除外する'
        parser.add_argument('query', help=help_msg)
        
        # 任意の引数
        help_msg =  'ツイート数 (default: %(default)s)\n' + \
                    '表示したいツイートの数\n' + \
                    '18000件を超過した場合はレート制限により18000件ごとに15分の待機時間が発生する'
        parser.add_argument('-t', '--num_of_tweets', type=int, default=100, help=help_msg)
        
        args: argparse.Namespace = parser.parse_args()
    except Exception as e:
        raise(e)
    
    return args


def __validate_args(args: argparse.Namespace) -> bool:
    '''引数検証'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = pyl.get_logger(__name__)
        
        # 検証：クエリが1文字以上であること
        if len(args.query) < 1:
            pyl.log_war(lg, f'クエリが1文字以上ではありません。(query:{args.query})')
            return False
        
        # 検証：ツイート数が1件以上であること
        if int(args.num_of_tweets) < 1:
            pyl.log_war(lg, f'ツイート数が1件以上ではありません。(num_of_tweets:{args.num_of_tweets})')
            return False
    except Exception as e:
        raise(e)
    
    return True


if __name__ == '__main__':
    sys.exit(main())

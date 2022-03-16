import argparse
import os
import sys
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth, twitter_tweet_stream


def main() -> int:
    
    '''
    メイン
    
    Summary:
        コマンドラインから実行する。
        
        引数を検証して問題ない場合、指定したキーワードのツイートを配信する。
    
    Args:
        -
    
    Args on cmd line:
        twitter_user_id_for_followees (str) : [グループAで1つのみ必須] TwitterユーザID(フォロイー用)
        twitter_list_id (str)               : [グループAで1つのみ必須] TwitterリストID
        keyword_of_csv_format (str)         : [任意] キーワード(csv形式)
    
    Returns:
        int: 終了コード(0：正常、1：異常)
    '''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        
        # 実行コマンドの表示
        sys.argv[0] = os.path.basename(sys.argv[0])
        pyl.log_inf(lg, f'実行コマンド：{sys.argv}')
        
        # 引数の取得・検証
        args: argparse.Namespace = __get_args()
        if __validate_args(args) == False:
            return 1
        
        # ロジック(TwitterAPI認証)の実行
        api: tweepy.API = twitter_api_auth.do_logic_that_generate_api_by_oauth_1_user()
        
        # ロジック(ツイート配信)の実行
        if args.twitter_user_id_for_followees is not None:
            twitter_tweet_stream.do_logic(
                    api,
                    args.twitter_user_id_for_followees,
                    args.keyword_of_csv_format,
                    stream_by_twitter_list_id=False
                )
        elif args.twitter_list_id is not None:
            twitter_tweet_stream.do_logic(
                    api,
                    args.twitter_list_id,
                    args.keyword_of_csv_format,
                    stream_by_twitter_list_id=True
                )
    except KeyboardInterrupt as e:
        if lg is not None:
            pyl.log_inf(lg, f'処理を中断しました。')
    except Exception as e:
        if lg is not None:
            pyl.log_exc(lg, '')
        return 1
    
    return 0


def __get_args() -> argparse.Namespace:
    '''引数取得'''
    
    try:
        parser: pyl.CustomArgumentParser = pyl.CustomArgumentParser(
                description='Twitterツイート配信\n' +
                            '指定したキーワードのツイートを配信します',
                formatter_class=argparse.RawTextHelpFormatter,
                exit_on_error=True
            )
        
        help_msg: str = ''
        
        # グループAの引数
        arg_group_a: argparse._ArgumentGroup = parser.add_argument_group(
            'options in this group', '処理対象のIDを指定します')
        mutually_exclusive_group_a: argparse._MutuallyExclusiveGroup = \
            arg_group_a.add_mutually_exclusive_group(required=True)
        help_msg =  '[1つのみ必須] {0}\n{1}'
        mutually_exclusive_group_a.add_argument(
            '-u', '--twitter_user_id_for_followees',
            type=str,
            help=help_msg.format(
                'TwitterユーザID(フォロイー用)', '指定したTwitterユーザIDのフォロイーのツイートを配信する'))
        mutually_exclusive_group_a.add_argument(
            '-l', '--twitter_list_id',
            type=str,
            help=help_msg.format(
                'TwitterリストID', '指定したTwitterリストIDのツイートを配信する'))
        
        # 任意の引数
        help_msg =  '[任意] キーワード(csv形式)\n' + \
                    '例："Google Docs, Google Drive"\n' + \
                    'スペースはAND検索(Google AND Docs)\n' + \
                    'カンマはOR検索(Google Docs OR Google Drive)'
        parser.add_argument('-k', '--keyword_of_csv_format', type=str, default='', help=help_msg)
        
        args: argparse.Namespace = parser.parse_args()
    except Exception as e:
        raise(e)
    
    return args


def __validate_args(args: argparse.Namespace) -> bool:
    '''引数検証'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        
        # 検証：グループAの引数が指定された場合は1文字以上であること
        if args.twitter_user_id_for_followees is not None \
            and not (len(args.twitter_user_id_for_followees) >= 1):
            pyl.log_war(lg, f'TwitterユーザID(フォロイー用)が1文字以上ではありません。' +
                            f'(twitter_user_id_for_followees:{args.twitter_user_id_for_followees})')
            return False
        elif args.twitter_list_id is not None \
            and not (len(args.twitter_list_id) >= 1):
            pyl.log_war(lg, f'TwitterリストIDが1文字以上ではありません。' +
                            f'(twitter_list_id:{args.twitter_list_id})')
            return False
    except Exception as e:
        raise(e)
    
    return True


if __name__ == '__main__':
    sys.exit(main())

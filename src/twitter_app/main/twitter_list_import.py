import argparse
import os
import sys
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth, twitter_list_import


def main() -> int:
    
    '''
    メイン
    
    Summary:
        コマンドラインから実行する。
        
        引数を検証して問題ない場合、Twitterリストをインポートする。
    
    Args:
        -
    
    Args on cmd line:
        twitter_list_file_path (str)    : [任意] Twitterリストファイルパス
        header_line_num (int)           : [任意] ヘッダ行番号
    
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
        api: tweepy.API = twitter_api_auth.do_logic_of_api_by_oauth_1_user()
        
        # ロジック(Twitterリストインポート)の実行
        twitter_list_import.do_logic(
                api,
                args.twitter_list_file_path,
                int(args.header_line_num)
            )
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
        
        # 任意の引数
        help_msg =  'Twitterリストファイルパス(csv) (default: %(default)s)\n' + \
                    'ワイルドカード可'
        parser.add_argument('-t', '--twitter_list_file_path', default='input/*.csv', help=help_msg)
        help_msg =  'ヘッダ行番号 (default: %(default)s)\n' + \
                    '0：ヘッダなし、1~：ヘッダとなるファイルの行番号'
        parser.add_argument('-hd', '--header_line_num', type=int, default='1', help=help_msg)
        
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
        
        # 検証：TwitterリストファイルパスがCSVファイルのパスであること
        twitter_list_file_path: tuple[str, str] = os.path.splitext(args.twitter_list_file_path)
        if twitter_list_file_path[1] != '.csv':
            pyl.log_war(lg, f'TwitterリストファイルパスがCSVファイルのパスではありません。' +
                            f'(twitter_list_file_path:{args.twitter_list_file_path})')
            return False
        
        # 検証：ヘッダ行番号が0以上であること
        if int(args.header_line_num) < 0:
            pyl.log_war(lg, f'ヘッダ行番号が0以上ではありません。' +
                            f'(header_line_num:{args.header_line_num})')
            return False
    except Exception as e:
        raise(e)
    
    return True


if __name__ == '__main__':
    sys.exit(main())

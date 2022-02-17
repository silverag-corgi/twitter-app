import argparse
import os
import sys
from logging import Logger
from typing import Optional

import python_lib_for_me as mylib
import tweepy
from twitter_lib_for_me.logic import api_auth, followee_twitter_list_gen


def main() -> int:
    
    '''
    メイン
    
    Summary:
        コマンドラインから実行する。
        
        引数を検証して問題ない場合、指定したユーザのフォロイーのTwitterリストを生成する。
    
    Args:
        -
    
    Args on cmd line:
        user_id (str)   : [必須] ユーザID(Twitter)
    
    Returns:
        int: 終了コード(0：正常、1：異常)
    '''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = mylib.get_logger(__name__)
        
        # 実行コマンド表示
        sys.argv[0] = os.path.basename(sys.argv[0])
        lg.info(f'実行コマンド：{sys.argv}')
        
        # 引数取得＆検証
        args: argparse.Namespace = __get_args()
        if __validate_args(args) == False:
            return 1
        
        # Twitter認証ロジックの実行
        api: tweepy.API = api_auth.do_logic()
        
        # フォロイーTwitterリスト生成ロジックの実行
        followee_twitter_list_gen.do_logic(
                api,
                args.user_id
            )
    except Exception as e:
        if lg is not None:
            lg.exception('', exc_info=True)
        return 1
    
    return 0


def __get_args() -> argparse.Namespace:
    '''引数取得'''
    
    try:
        parser: argparse.ArgumentParser = argparse.ArgumentParser(
                formatter_class=argparse.RawTextHelpFormatter,
                exit_on_error=True
            )
        
        # 必須の引数
        help_msg = 'ユーザID(Twitter)'
        parser.add_argument('user_id', help=help_msg)
        
        args: argparse.Namespace = parser.parse_args()
    except Exception as e:
        raise(e)
    
    return args


def __validate_args(args: argparse.Namespace) -> bool:
    '''引数検証'''
    
    lg: Optional[Logger] = None
    
    try:
        # ロガー取得
        lg = mylib.get_logger(__name__)
        
        # 検証：なし
    except Exception as e:
        raise(e)
    
    return True


if __name__ == '__main__':
    sys.exit(main())

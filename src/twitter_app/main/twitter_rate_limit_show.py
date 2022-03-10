import argparse
import os
import sys
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth
from twitter_app.util.twitter_api_standard_v1_1 import twitter_developer_util


def main() -> int:
    
    '''
    メイン
    
    Summary:
        コマンドラインから実行する。
        
        引数を検証して問題ない場合、レート制限を表示する。
    
    Args:
        -
    
    Args on cmd line:
        resource_family (str)   : [必須] リソース群
        endpoint (str)          : [必須] エンドポイント
    
    Returns:
        int: 終了コード(0：正常、1：異常)
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
        
        # レート制限の表示
        twitter_developer_util.show_rate_limit(api, args.resource_family, args.endpoint)
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
        help_msg =  'リソース群\n' + \
                    '例：application'
        parser.add_argument('resource_family', help=help_msg)
        help_msg =  'エンドポイント\n' + \
                    '例：/application/rate_limit_status\n' + \
                    '両方とも空文字の場合は全てのレート制限を表示します'
        parser.add_argument('endpoint', help=help_msg)
        
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
        
        # 検証：なし
    except Exception as e:
        raise(e)
    
    return True


if __name__ == '__main__':
    sys.exit(main())

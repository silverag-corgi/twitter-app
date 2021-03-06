import argparse
import os
import sys
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl

from twitter_app.logic import twitter_api_auth


def main() -> int:
    
    '''
    メイン
    
    Summary:
        コマンドラインから実行する。
        
        コンシューマーキーとPINコードを基にアクセストークンを生成し、認証情報ファイルに保存する。
    
    Args:
        -
    
    Args on cmd line:
        -
    
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
        twitter_api_auth.do_logic_that_generate_api_by_oauth_1_user_using_pin()
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
                description='TwitterPIN認証\n' +
                            'コンシューマーキーとPINコードを基にアクセストークンを生成し、認証情報ファイルに保存します',
                formatter_class=argparse.RawTextHelpFormatter,
                exit_on_error=True
            )
        
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
        
        # 検証：なし
    except Exception as e:
        raise(e)
    
    return True


if __name__ == '__main__':
    sys.exit(main())

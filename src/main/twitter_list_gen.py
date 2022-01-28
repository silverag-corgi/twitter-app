import argparse
import sys
from logging import Logger

import python_lib_for_me
import tweepy
from src.logic import api_auth, twitter_list_gen


def main():
    '''メイン'''

    try:
        # ロガー取得
        logger: Logger = python_lib_for_me.get_logger(__name__)
        
        # 引数取得
        args: argparse.Namespace = __get_args()
        if __validate_args(args) == False:
            return 1

        # Twitter認証実行
        api: tweepy.API = api_auth.do_logic()

        # Twitterリスト作成
        twitter_list_gen.do_logic(api, args.csv_file_path)
    except Exception as e:
        logger.exception("", exc_info=True)
        return 1
    
    return 0


def __get_args() -> argparse.Namespace:
    '''引数取得'''

    try:
        parser: argparse.ArgumentParser = argparse.ArgumentParser(exit_on_error=False)
        parser.add_argument('-csv', '--csv_file_path',
                            default='input/*.csv',
                            help='csv file path (regex enabled) (default: %(default)s)')
        args: argparse.Namespace = parser.parse_args()
    except Exception as e:
        raise(e)

    return args


def __validate_args(args: argparse.Namespace) -> bool:
    '''引数検証'''

    try:
        # ロガー取得
        logger: Logger = python_lib_for_me.get_logger(__name__)
            
        # 検証：CSVファイルのパスであること
        if not '.csv' in args.csv_file_path:
            logger.info(f'CSVファイルのパスではありません。(パス：{args.csv_file_path})')
            return False
    except Exception as e:
        raise(e)

    return True


if __name__ == '__main__':
    sys.exit(main())

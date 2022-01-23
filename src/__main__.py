import argparse
import sys
import traceback

import tweepy

from src import api_auth, twitter_list_gen


def main():
    '''メイン'''

    try:
        # 引数取得
        args: argparse.Namespace = __get_args()
        if __validate_args(args) == False:
            return 1

        # Twitter認証実行
        api: tweepy.API = api_auth.do_logic()

        # Twitterリスト作成
        twitter_list_gen.do_logic(api, args.csv_file_path)
    except Exception as e:
        print(traceback.format_exc())
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

    # 検証：CSVファイルのパスであること
    if not '.csv' in args.csv_file_path:
        print(f'CSVファイルのパスではありません。(パス：{args.csv_file_path})')
        return False

    return True


sys.exit(main())

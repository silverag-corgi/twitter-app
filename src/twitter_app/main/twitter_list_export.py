import argparse
import os
import sys
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth, twitter_list_export


def main() -> int:
    
    '''
    メイン
    
    Summary:
        コマンドラインから実行する。
        
        引数を検証して問題ない場合、指定したTwitterリストをTwitterからエクスポートする。
    
    Args:
        -
    
    Args on cmd line:
        show_twitter_list (bool)    : [グループAで1つのみ必須] Twitterリスト表示要否
        export_twitter_list (bool)  : [グループAで1つのみ必須] Twitterリストエクスポート要否
        all_twitter_list (bool)     : [グループBで1つのみ必須] 全てのTwitterリスト
        twitter_list_id (str)       : [グループBで1つのみ必須] TwitterリストID(csv形式)
        twitter_list_name (str)     : [グループBで1つのみ必須] Twitterリスト名(csv形式)
    
    Returns:
        int: 終了コード(0：正常、1：異常)
    
    Destinations:
        Twitterリストファイル: ./dest/twitter_list/twitter_list_[Twitterリスト名].csv
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
        
        # ロジックの実行
        if bool(args.show_twitter_list) == True:
            # ロジック(Twitterリスト表示)の実行
            if bool(args.all_twitter_list) == True:
                twitter_list_export.do_logic_that_show_twitter_list(
                        api,
                        twitter_list_export.TWITTER_LIST_PROC_TARGET.ALL,
                        ''
                    )
            elif args.twitter_list_id is not None:
                twitter_list_export.do_logic_that_show_twitter_list(
                        api,
                        twitter_list_export.TWITTER_LIST_PROC_TARGET.ID,
                        args.twitter_list_id
                    )
            elif args.twitter_list_name is not None:
                twitter_list_export.do_logic_that_show_twitter_list(
                        api,
                        twitter_list_export.TWITTER_LIST_PROC_TARGET.NAME,
                        args.twitter_list_name
                    )
        elif bool(args.export_twitter_list) == True:
            # ロジック(Twitterリストエクスポート)の実行
            if bool(args.all_twitter_list) == True:
                twitter_list_export.do_logic_that_export_twitter_list(
                        api,
                        twitter_list_export.TWITTER_LIST_PROC_TARGET.ALL,
                        ''
                    )
            elif args.twitter_list_id is not None:
                twitter_list_export.do_logic_that_export_twitter_list(
                        api,
                        twitter_list_export.TWITTER_LIST_PROC_TARGET.ID,
                        args.twitter_list_id
                    )
            elif args.twitter_list_name is not None:
                twitter_list_export.do_logic_that_export_twitter_list(
                        api,
                        twitter_list_export.TWITTER_LIST_PROC_TARGET.NAME,
                        args.twitter_list_name
                    )
    except Exception as e:
        if lg is not None:
            pyl.log_exc(lg, '')
        return 1
    
    return 0


def __get_args() -> argparse.Namespace:
    '''引数取得'''
    
    try:
        parser: pyl.CustomArgumentParser = pyl.CustomArgumentParser(
                description='Twitterリストエクスポート\n' +
                            '指定したTwitterリストをTwitterからエクスポートする',
                formatter_class=argparse.RawTextHelpFormatter,
                exit_on_error=True
            )
        
        help_msg: str = ''
        
        # グループAの引数
        arg_group_a: argparse._ArgumentGroup = parser.add_argument_group(
            'グループA', '実行する処理を選択する')
        mutually_exclusive_group_a: argparse._MutuallyExclusiveGroup = \
            arg_group_a.add_mutually_exclusive_group(required=True)
        help_msg =  '[1つのみ必須] {0}\n{1}'
        mutually_exclusive_group_a.add_argument(
            '-s', '--show_twitter_list',
            action='store_true',
            help=help_msg.format(
                'Twitterリスト表示要否', '指定した場合はTwitterリストを表示する'))
        mutually_exclusive_group_a.add_argument(
            '-e', '--export_twitter_list',
            action='store_true',
            help=help_msg.format(
                'Twitterリストエクスポート要否', '指定した場合はTwitterリストをエクスポートする'))
        
        # グループBの引数
        arg_group_b: argparse._ArgumentGroup = parser.add_argument_group(
            'グループB', '処理対象のTwitterリストを選択する')
        mutually_exclusive_group_b: argparse._MutuallyExclusiveGroup = \
            arg_group_b.add_mutually_exclusive_group(required=True)
        help_msg =  '[1つのみ必須] {0}\n{1}'
        mutually_exclusive_group_b.add_argument(
            '-all', '--all_twitter_list',
            action='store_true',
            help=help_msg.format('全てのTwitterリスト', ''))
        mutually_exclusive_group_b.add_argument(
            '-id', '--twitter_list_id',
            type=str,
            help=help_msg.format(
                'TwitterリストID (csv形式)', '例："0123456789111111111, 0123456789222222222"'))
        mutually_exclusive_group_b.add_argument(
            '-name', '--twitter_list_name',
            type=str,
            help=help_msg.format(
                'Twitterリスト名 (csv形式)', '例："Google関連アカウント, Microsoft関連アカウント"'))
        
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
        
        # 検証：グループBの引数が指定された場合は1文字以上であること
        if args.twitter_list_id is not None \
            and not (len(args.twitter_list_id) >= 1):
            pyl.log_war(lg, f'TwitterリストIDが1文字以上ではありません。' +
                            f'(twitter_list_id:{args.twitter_list_id})')
            return False
        elif args.twitter_list_name is not None \
            and not (len(args.twitter_list_name) >= 1):
            pyl.log_war(lg, f'Twitterリスト名が1文字以上ではありません。' +
                            f'(twitter_list_name:{args.twitter_list_name})')
            return False
    except Exception as e:
        raise(e)
    
    return True


if __name__ == '__main__':
    sys.exit(main())

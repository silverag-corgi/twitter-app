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
        
        引数を検証して問題ない場合、指定したリストをTwitterからエクスポートする。
    
    Args:
        -
    
    Args on cmd line:
        show_list (bool)    : [グループAで1つのみ必須] リスト表示要否
        export_list (bool)  : [グループAで1つのみ必須] リストエクスポート要否
        all_list (bool)     : [グループBで1つのみ必須] 全てのリスト
        list_id (str)       : [グループBで1つのみ必須] リストID(csv形式)
        list_name (str)     : [グループBで1つのみ必須] リスト名(csv形式)
    
    Returns:
        int: 終了コード(0：正常、1：異常)
    
    Destinations:
        リストメンバーファイル: ./dest/list_member/[リスト名].csv
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
        
        # ロジックの実行
        if bool(args.show_list) == True:
            # ロジック(Twitterリスト表示)の実行
            if bool(args.all_list) == True:
                twitter_list_export.do_logic_that_show_list(
                        api,
                        twitter_list_export.EnumOfListProcTarget.ALL,
                        ''
                    )
            elif args.list_id is not None:
                twitter_list_export.do_logic_that_show_list(
                        api,
                        twitter_list_export.EnumOfListProcTarget.ID,
                        args.list_id
                    )
            elif args.list_name is not None:
                twitter_list_export.do_logic_that_show_list(
                        api,
                        twitter_list_export.EnumOfListProcTarget.NAME,
                        args.list_name
                    )
        elif bool(args.export_list) == True:
            # ロジック(Twitterリストエクスポート)の実行
            if bool(args.all_list) == True:
                twitter_list_export.do_logic_that_export_list(
                        api,
                        twitter_list_export.EnumOfListProcTarget.ALL,
                        ''
                    )
            elif args.list_id is not None:
                twitter_list_export.do_logic_that_export_list(
                        api,
                        twitter_list_export.EnumOfListProcTarget.ID,
                        args.list_id
                    )
            elif args.list_name is not None:
                twitter_list_export.do_logic_that_export_list(
                        api,
                        twitter_list_export.EnumOfListProcTarget.NAME,
                        args.list_name
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
                            '指定したリストをTwitterからエクスポートします',
                formatter_class=argparse.RawTextHelpFormatter,
                exit_on_error=True
            )
        
        help_msg: str = ''
        
        # グループAの引数
        arg_group_a: argparse._ArgumentGroup = parser.add_argument_group(
            'options in this group', '実行する処理を指定します')
        mutually_exclusive_group_a: argparse._MutuallyExclusiveGroup = \
            arg_group_a.add_mutually_exclusive_group(required=True)
        help_msg =  '[1つのみ必須] {0}\n{1}'
        mutually_exclusive_group_a.add_argument(
            '-s', '--show_list',
            action='store_true',
            help=help_msg.format(
                'リスト表示要否', '指定した場合はリストを表示します'))
        mutually_exclusive_group_a.add_argument(
            '-e', '--export_list',
            action='store_true',
            help=help_msg.format(
                'リストエクスポート要否', '指定した場合はリストをエクスポートします'))
        
        # グループBの引数
        arg_group_b: argparse._ArgumentGroup = parser.add_argument_group(
            'options in this group', '処理対象のリストを指定します')
        mutually_exclusive_group_b: argparse._MutuallyExclusiveGroup = \
            arg_group_b.add_mutually_exclusive_group(required=True)
        help_msg =  '[1つのみ必須] {0}\n{1}'
        mutually_exclusive_group_b.add_argument(
            '-all', '--all_list',
            action='store_true',
            help=help_msg.format('全てのリスト', ''))
        mutually_exclusive_group_b.add_argument(
            '-id', '--list_id',
            type=str,
            help=help_msg.format(
                'リストID(csv形式)', '例："0123456789111111111, 0123456789222222222"'))
        mutually_exclusive_group_b.add_argument(
            '-name', '--list_name',
            type=str,
            help=help_msg.format(
                'リスト名(csv形式)', '例："Google関連アカウント, Microsoft関連アカウント"'))
        
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
        if args.list_id is not None \
            and not (len(args.list_id) >= 1):
            pyl.log_war(lg, f'リストIDが1文字以上ではありません。' +
                            f'(list_id:{args.list_id})')
            return False
        elif args.list_name is not None \
            and not (len(args.list_name) >= 1):
            pyl.log_war(lg, f'リスト名が1文字以上ではありません。' +
                            f'(list_name:{args.list_name})')
            return False
    except Exception as e:
        raise(e)
    
    return True


if __name__ == '__main__':
    sys.exit(main())

import argparse
import os
import sys
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth, twitter_followxx_export


def main() -> int:
    
    '''
    メイン
    
    Summary:
        コマンドラインから実行する。
        
        引数を検証して問題ない場合、指定したユーザのフォロイー(フォロワー)をエクスポートする。
    
    Args:
        -
    
    Args on cmd line:
        user_id (str)           : [必須] ユーザID
        followee (bool)         : [グループAで1つのみ必須] フォロイー
        follower (bool)         : [グループAで1つのみ必須] フォロワー
        num_of_followxxs (int)  : [任意] フォロイー(フォロワー)数
    
    Returns:
        int: 終了コード(0：正常、1：異常)
    
    Destinations:
        フォロイーファイル: ./dest/followee/[ユーザID].csv
        フォロワーファイル: ./dest/follower/[ユーザID].csv
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
        
        # ロジック(Twitterフォロイー(フォロワー)エクスポート)の実行
        if bool(args.followee) == True:
            # ロジック(Twitterフォロイーエクスポート)の実行
            twitter_followxx_export.do_logic(
                    api,
                    args.user_id,
                    args.num_of_followxxs,
                    twitter_followxx_export.EnumOfItemProcTarget.FOLLOWEE
                )
        elif bool(args.follower) == True:
            # ロジック(Twitterフォロワーエクスポート)の実行
            twitter_followxx_export.do_logic(
                    api,
                    args.user_id,
                    args.num_of_followxxs,
                    twitter_followxx_export.EnumOfItemProcTarget.FOLLOWER
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
                description='Twitterフォロイー(フォロワー)エクスポート\n' +
                            '指定したユーザのフォロイー(フォロワー)をエクスポートします',
                formatter_class=argparse.RawTextHelpFormatter,
                exit_on_error=True
            )
        
        # 必須の引数
        help_msg = '[必須] ユーザID'
        parser.add_argument('user_id', help=help_msg)
        
        # グループAの引数
        arg_group_a: argparse._ArgumentGroup = parser.add_argument_group(
            'options in this group', '処理対象の項目を指定します')
        mutually_exclusive_group_a: argparse._MutuallyExclusiveGroup = \
            arg_group_a.add_mutually_exclusive_group(required=True)
        help_msg =  '[1つのみ必須] {0}\n' + \
                    '{1}をエクスポートします'
        mutually_exclusive_group_a.add_argument(
            '-e', '--followee',
            action='store_true',
            help=help_msg.format('フォロイー', 'フォロイー(指定したユーザがフォローしているユーザ)'))
        mutually_exclusive_group_a.add_argument(
            '-r', '--follower',
            action='store_true',
            help=help_msg.format('フォロワー', 'フォロワー(指定したユーザをフォローしているユーザ)'))
        
        # 任意の引数
        help_msg =  '[任意] フォロイー(フォロワー)数 (デフォルト：%(default)s)\n' + \
                    'エクスポートしたいフォロイー(フォロワー)の人数\n' + \
                    '3000人を超過した場合はレート制限により3000人ごとに15分の待機時間が発生します'
        parser.add_argument('-f', '--num_of_followxxs', type=int, default=3000, help=help_msg)
        
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
        
        # 検証：ユーザIDが4文字以上であること
        if not (len(args.user_id) >= 4):
            pyl.log_war(lg, f'ユーザIDが4文字以上ではありません。' +
                            f'(user_id:{args.user_id})')
            return False
        
        # 検証：フォロイー(フォロワー)数が1人以上であること
        if not (int(args.num_of_followxxs) >= 1):
            pyl.log_war(lg, f'フォロイー(フォロワー)数が1人以上ではありません。' +
                            f'(num_of_followxxs:{args.num_of_followxxs})')
            return False
    except Exception as e:
        raise(e)
    
    return True


if __name__ == '__main__':
    sys.exit(main())

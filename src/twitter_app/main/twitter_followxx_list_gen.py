import argparse
import os
import sys
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_app.logic import twitter_api_auth, twitter_followxx_list_gen


def main() -> int:
    
    '''
    メイン
    
    Summary:
        コマンドラインから実行する。
        
        引数を検証して問題ない場合、指定したユーザのフォロイー(フォロワー)のリストを生成する。
    
    Args:
        -
    
    Args on cmd line:
        user_id (str)                   : [必須] ユーザID
        generate_followee_list (bool)   : [グループAで1つのみ必須] フォロイーリスト生成
        generate_follower_list (bool)   : [グループAで1つのみ必須] フォロワーリスト生成
        num_of_followxxs (int)          : [任意] フォロイー(フォロワー)数
    
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
        
        # ロジック(Twitterフォロイー(フォロワー)リスト生成)の実行
        if bool(args.generate_followee_list) == True:
            # ロジック(Twitterフォロイーリスト生成)の実行
            twitter_followxx_list_gen.do_logic(
                    api,
                    args.user_id,
                    args.num_of_followxxs,
                    twitter_followxx_list_gen.EnumOfFollowxxList.FOLLOWEE_LIST
                )
        elif bool(args.generate_follower_list) == True:
            # ロジック(Twitterフォロワーリスト生成)の実行
            twitter_followxx_list_gen.do_logic(
                    api,
                    args.user_id,
                    args.num_of_followxxs,
                    twitter_followxx_list_gen.EnumOfFollowxxList.FOLLOWER_LIST
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
                description='Twitterフォロイー(フォロワー)リスト生成\n' +
                            '指定したユーザのフォロイー(フォロワー)のリストを生成します',
                formatter_class=argparse.RawTextHelpFormatter,
                exit_on_error=True
            )
        
        # 必須の引数
        help_msg = '[必須] ユーザID'
        parser.add_argument('user_id', help=help_msg)
        
        # グループAの引数
        arg_group_a: argparse._ArgumentGroup = parser.add_argument_group(
            'options in this group', '実行する処理を指定します')
        mutually_exclusive_group_a: argparse._MutuallyExclusiveGroup = \
            arg_group_a.add_mutually_exclusive_group(required=True)
        help_msg =  '[1つのみ必須] {0}\n' + \
                    '指定した場合は{1}のリストを生成します'
        mutually_exclusive_group_a.add_argument(
            '-followee', '--generate_followee_list',
            action='store_true',
            help=help_msg.format('フォロイーリスト生成', 'フォロイー'))
        mutually_exclusive_group_a.add_argument(
            '-follower', '--generate_follower_list',
            action='store_true',
            help=help_msg.format('フォロワーリスト生成', 'フォロワー'))
        
        # 任意の引数
        help_msg =  '[任意] フォロイー(フォロワー)数 (デフォルト：%(default)s)\n' + \
                    'リストに追加したいフォロイー(フォロワー)の人数\n' + \
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

import argparse
import os
import sys
from logging import Logger
from typing import Optional

import python_lib_for_me as pyl
import tweepy

from twitter_lib_for_me.logic import api_auth, followxx_twitter_list_gen


def main() -> int:
    
    '''
    メイン
    
    Summary:
        コマンドラインから実行する。
        
        引数を検証して問題ない場合、指定したユーザのフォロイー／フォロワーのTwitterリストを生成する。
    
    Args:
        -
    
    Args on cmd line:
        user_id (str)                   : [必須] ユーザID(Twitter)
        generate_followee_list (bool)   : [いずれかが必須] フォロイーリスト生成
        generate_follower_list (bool)   : [いずれかが必須] フォロワーリスト生成
        num_of_followxxs (int)          : [任意] フォロイー数／フォロワー数
    
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
        
        # Twitter認証ロジックの実行
        api: tweepy.API = api_auth.do_logic()
        
        # Twitterリスト生成ロジックの実行
        if bool(args.generate_followee_list) == True:
            # フォロイーTwitterリスト生成ロジックの実行
            followxx_twitter_list_gen.do_logic(
                    api,
                    args.user_id,
                    args.num_of_followxxs,
                    followxx_twitter_list_gen.Pages.followee_list
                )
        elif bool(args.generate_follower_list) == True:
            # フォロワーTwitterリスト生成ロジックの実行
            followxx_twitter_list_gen.do_logic(
                    api,
                    args.user_id,
                    args.num_of_followxxs,
                    followxx_twitter_list_gen.Pages.follower_list
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
        
        # 必須の引数
        help_msg = 'ユーザID(Twitter)'
        parser.add_argument('user_id', help=help_msg)
        
        # グループで1つのみ必須の引数
        group: argparse._MutuallyExclusiveGroup = parser.add_mutually_exclusive_group(required=True)
        help_msg =  '{0}\n' + \
                    'グループで1つのみ必須\n' + \
                    '指定した場合は{1}のTwitterリストを生成する'
        group.add_argument(
            '-followee', '--generate_followee_list',
            help=help_msg.format('フォロイーリスト生成', 'フォロイー'), action='store_true')
        group.add_argument(
            '-follower', '--generate_follower_list',
            help=help_msg.format('フォロワーリスト生成', 'フォロワー'), action='store_true')
        
        # 任意の引数
        help_msg =  'フォロイー数／フォロワー数 (default: %(default)s)\n' + \
                    'Twitterリストに追加したいフォロイー／フォロワーの人数\n' + \
                    '3000人を超過した場合はレート制限により3000人ごとに15分の待機時間が発生する'
        parser.add_argument('-f', '--num_of_followxxs', type=int, default=3000, help=help_msg)
        
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

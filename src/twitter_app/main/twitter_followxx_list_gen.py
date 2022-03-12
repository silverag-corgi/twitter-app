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
        
        引数を検証して問題ない場合、指定したユーザのフォロイー(フォロワー)のTwitterリストを生成する。
    
    Args:
        -
    
    Args on cmd line:
        user_id (str)                   : [必須] ユーザID(Twitter)
        generate_followee_list (bool)   : [いずれかが必須] フォロイーリスト生成
        generate_follower_list (bool)   : [いずれかが必須] フォロワーリスト生成
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
        api: tweepy.API = twitter_api_auth.do_logic_of_api_by_oauth_1_user()
        
        # ロジック(Twitterリスト生成)の実行
        if bool(args.generate_followee_list) == True:
            # ロジック(Twitterフォロイーリスト生成)の実行
            twitter_followxx_list_gen.do_logic(
                    api,
                    args.user_id,
                    args.num_of_followxxs,
                    twitter_followxx_list_gen.Pages.FOLLOWEE_LIST
                )
        elif bool(args.generate_follower_list) == True:
            # ロジック(Twitterフォロワーリスト生成)の実行
            twitter_followxx_list_gen.do_logic(
                    api,
                    args.user_id,
                    args.num_of_followxxs,
                    twitter_followxx_list_gen.Pages.FOLLOWER_LIST
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
        help_msg =  'フォロイー(フォロワー)数 (default: %(default)s)\n' + \
                    'Twitterリストに追加したいフォロイー(フォロワー)の人数\n' + \
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
        # ロガーの取得
        lg = pyl.get_logger(__name__)
        
        # 検証：ユーザIDが4文字以上であること
        if len(args.user_id) < 4:
            pyl.log_war(lg, f'ユーザIDが4文字以上ではありません。(user_id:{args.user_id})')
            return False
        
        # 検証：フォロイー(フォロワー)数が1人以上であること
        if int(args.num_of_followxxs) < 1:
            pyl.log_war(lg, f'フォロイー(フォロワー)数が1人以上ではありません。' +
                            f'(num_of_followxxs:{args.num_of_followxxs})')
            return False
    except Exception as e:
        raise(e)
    
    return True


if __name__ == '__main__':
    sys.exit(main())

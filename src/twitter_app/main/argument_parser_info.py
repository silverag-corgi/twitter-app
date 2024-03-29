import argparse
import textwrap
from typing import Final

from twitter_app.main.sub_commands import (
    twitter_api_auth,
    twitter_followxx_export,
    twitter_list_export,
    twitter_list_import,
    twitter_list_show,
    twitter_rate_limit_show,
    twitter_tweet_search,
    twitter_tweet_stream,
)

DESC_OF_AUTH_API: Final[str] = textwrap.dedent(
    """\
    - 機能名
        - TwitterAPI認証
    - 概要
        - コンシューマーキーとPINコードを基にアクセストークンを生成し、認証情報ファイルに保存します
    - 生成ファイル
        - TwitterAPI認証情報ファイル
            - config/twitter_api_auth_info.json
    - コマンド例
        - poetry run twitter auth-api
    """
)

DESC_OF_EXP_FOLLOWXX: Final[str] = textwrap.dedent(
    """\
    - 機能名
        - Twitterフォロイー(フォロワー)エクスポート
    - 概要
        - 指定したユーザのフォロイー(フォロワー)をエクスポートします
    - 生成ファイル
        - フォロイーファイル
            - ./dest/followee/[ユーザID].csv
        - フォロワーファイル
            - ./dest/follower/[ユーザID].csv
    - コマンド例
        - poetry run twitter exp-followxx "silverag_corgi" -e -f 3000
        - poetry run twitter exp-followxx "silverag_corgi" -r -f 3000
    """
)

DESC_OF_EXP_LIST: Final[str] = textwrap.dedent(
    """\
    - 機能名
        - Twitterリストエクスポート
    - 概要
        - 指定したリストをTwitterからエクスポートします
    - 生成ファイル
        - リストメンバーファイル
            - ./dest/list_member/[リスト名].csv
    - コマンド例
        - poetry run twitter exp-list -all
        - poetry run twitter exp-list -id "0123456789111111111, 0123456789222222222"
        - poetry run twitter exp-list -name "Google関連, Microsoft関連"
    """
)

DESC_OF_IMP_LIST: Final[str] = textwrap.dedent(
    """\
    - 機能名
        - Twitterリストインポート
    - 概要
        - 指定したcsvファイルをリストとしてTwitterにインポートします
    - コマンド例
        - poetry run twitter imp-list -l "input/list_member/*.csv" -hd 1 -d
    """
)

DESC_OF_SHOW_LIST: Final[str] = textwrap.dedent(
    """\
    - 機能名
        - Twitterリスト表示
    - 概要
        - 指定したリストを表示します
    - コマンド例
        - poetry run twitter show-list -all
        - poetry run twitter show-list -id "0123456789111111111, 0123456789222222222"
        - poetry run twitter show-list -name "Google関連, Microsoft関連"
    """
)

DESC_OF_SHOW_LIMIT: Final[str] = textwrap.dedent(
    """\
    - 機能名
        - Twitterレート制限表示
    - 概要
        - 指定したリソース群とエンドポイントのレート制限を表示します
    - コマンド例
        - poetry run twitter show-limit "friends" "/friends/list"
        - poetry run twitter show-limit "" ""
    """
)

DESC_OF_SEARCH_TWEET: Final[str] = textwrap.dedent(
    """\
    - 機能名
        - Twitterツイート検索
    - 概要
        - 指定したクエリでツイートを検索し、ツイート検索結果ファイルを生成します
    - 生成ファイル
        - ツイート検索結果ファイル
            - ./dest/tweet_search_result/[クエリ].csv
    - コマンド例
        - poetry run twitter search-tweet "API" -t 100
    """
)

DESC_OF_STREAM_TWEET: Final[str] = textwrap.dedent(
    """\
    - 機能名
        - Twitterツイート配信
    - 概要
        - 指定したキーワードのツイートを配信します
    - コマンド例
        - poetry run twitter stream-tweet -ui "silverag_corgi" -k "Google Docs, Google Drive"
        - poetry run twitter stream-tweet -li "0123456789111111111" -k "Google Docs, Google Drive"
        - poetry run twitter stream-tweet -ln "Google関連" -k "Google Docs, Google Drive"
        - poetry run twitter stream-tweet -fp "input/list_member/*.csv" 1 -k "Google Docs, Google Drive"
    """
)

ARGUMENT_PARSER_INFO_DICT: Final[dict] = {
    "description": textwrap.dedent(
        """\
        twitter-app
        TwitterAPIを利用したアプリケーション。
        """
    ),
    "formatter_class": argparse.RawTextHelpFormatter,
    "exit_on_error": True,
    "arguments": [
        {
            "name": ["-d", "--use_debug_mode"],
            "action": "store_true",
            "default": False,
            "help": "デバッグモード使用有無",
        },
    ],
    "subcommands": {
        "title": "sub_commands",
        "required": True,
        "commands": [
            {
                "name": ["auth-api"],
                "help": DESC_OF_AUTH_API,
                "description": DESC_OF_AUTH_API,
                "func": twitter_api_auth.authenticate_twitter_api,
                "formatter_class": argparse.RawTextHelpFormatter,
                "arguments": [],
            },
            {
                "name": ["exp-followxx"],
                "help": DESC_OF_EXP_FOLLOWXX,
                "description": DESC_OF_EXP_FOLLOWXX,
                "func": twitter_followxx_export.export_twitter_followxx,
                "formatter_class": argparse.RawTextHelpFormatter,
                "arguments": [
                    # グループA(必須)
                    {
                        "name": ["user_id"],
                        "type": str,
                        "help": textwrap.dedent(
                            """\
                            - [グループA(必須)] ユーザID
                            """  # noqa: E501
                        ),
                        # "group": "group_a (required)",
                    },
                    # グループB1(1つのみ必須)
                    {
                        "name": ["-e", "--export_followee"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] フォロイーエクスポート要否
                                - フォロイー(指定したユーザがフォローしているユーザ)をエクスポートします
                            """  # noqa: E501
                        ),
                        "exclusive_group": "group_b1 (exclusive)",
                    },
                    {
                        "name": ["-r", "--export_follower"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] フォロワーエクスポート要否
                                - フォロワー(指定したユーザをフォローしているユーザ)をエクスポートします
                            """  # noqa: E501
                        ),
                        "exclusive_group": "group_b1 (exclusive)",
                    },
                    # グループC(任意)
                    {
                        "name": ["-f", "--num_of_followxxs"],
                        "type": int,
                        "default": 3000,
                        "help": textwrap.dedent(
                            """\
                            - [グループC(任意)] フォロイー(フォロワー)数 (デフォルト：%(default)s)
                                - エクスポートするフォロイー(フォロワー)の人数
                                - 3000人を超過した場合はレート制限により3000人ごとに15分の待機時間が発生します
                            """  # noqa: E501
                        ),
                        # "group": "group_c (optional)",
                    },
                ],
            },
            {
                "name": ["exp-list"],
                "help": DESC_OF_EXP_LIST,
                "description": DESC_OF_EXP_LIST,
                "func": twitter_list_export.export_twitter_list,
                "formatter_class": argparse.RawTextHelpFormatter,
                "arguments": [
                    # グループB1(1つのみ必須)
                    {
                        "name": ["-all", "--all_list"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] 全てのリスト
                            """  # noqa: E501
                        ),
                        "exclusive_group": "group_b1 (exclusive)",
                    },
                    {
                        "name": ["-id", "--list_id"],
                        "type": str,
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] リストID(csv形式)
                                - 例："0123456789111111111, 0123456789222222222"
                            """  # noqa: E501
                        ),
                        "exclusive_group": "group_b1 (exclusive)",
                    },
                    {
                        "name": ["-name", "--list_name"],
                        "type": str,
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] リスト名(csv形式)
                                - 例："Google関連, Microsoft関連"
                            """  # noqa: E501
                        ),
                        "exclusive_group": "group_b1 (exclusive)",
                    },
                ],
            },
            {
                "name": ["imp-list"],
                "help": DESC_OF_IMP_LIST,
                "description": DESC_OF_IMP_LIST,
                "func": twitter_list_import.import_twitter_list,
                "formatter_class": argparse.RawTextHelpFormatter,
                "arguments": [
                    # グループC(任意)
                    {
                        "name": ["-l", "--list_member_file_path"],
                        "type": str,
                        "default": "input/list_member/*.csv",
                        "help": textwrap.dedent(
                            """\
                            - [グループC(任意)] リストメンバーファイルパス(csvファイル) (デフォルト：%(default)s)
                                - ワイルドカード可
                            """  # noqa: E501
                        ),
                        # "group": "group_c (optional)",
                    },
                    {
                        "name": ["-hd", "--header_line_num"],
                        "type": int,
                        "default": 1,
                        "help": textwrap.dedent(
                            """\
                            - [グループC(任意)] ヘッダ行番号 (デフォルト：%(default)s)
                                - 0：ヘッダなし
                                - 1~：ヘッダとなるファイルの行番号
                            """  # noqa: E501
                        ),
                        # "group": "group_c (optional)",
                    },
                    {
                        "name": ["-d", "--add_only_users_with_diff"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループC(任意)] 差分ユーザ追加
                                - 指定した場合は既存のリストに差分のあるユーザのみを追加します
                                - 指定しない場合は既存のリストを削除して新しいリストにユーザを追加します
                            """  # noqa: E501
                        ),
                        # "group": "group_c (optional)",
                    },
                ],
            },
            {
                "name": ["show-list"],
                "help": DESC_OF_SHOW_LIST,
                "description": DESC_OF_SHOW_LIST,
                "func": twitter_list_show.show_twitter_list,
                "formatter_class": argparse.RawTextHelpFormatter,
                "arguments": [
                    # グループB1(1つのみ必須)
                    {
                        "name": ["-all", "--all_list"],
                        "action": "store_true",
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] 全てのリスト
                            """  # noqa: E501
                        ),
                        "exclusive_group": "group_b1 (exclusive)",
                    },
                    {
                        "name": ["-id", "--list_id"],
                        "type": str,
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] リストID(csv形式)
                                - 例："0123456789111111111, 0123456789222222222"
                            """  # noqa: E501
                        ),
                        "exclusive_group": "group_b1 (exclusive)",
                    },
                    {
                        "name": ["-name", "--list_name"],
                        "type": str,
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] リスト名(csv形式)
                                - 例："Google関連, Microsoft関連"
                            """  # noqa: E501
                        ),
                        "exclusive_group": "group_b1 (exclusive)",
                    },
                ],
            },
            {
                "name": ["show-limit"],
                "help": DESC_OF_SHOW_LIMIT,
                "description": DESC_OF_SHOW_LIMIT,
                "func": twitter_rate_limit_show.show_rate_limit,
                "formatter_class": argparse.RawTextHelpFormatter,
                "arguments": [
                    # グループA(必須)
                    {
                        "name": ["resource_family"],
                        "type": str,
                        "help": textwrap.dedent(
                            """\
                            - [グループA(必須)] リソース群
                                - 例："friends"
                                - 例："" (両方とも空文字の場合は全てのレート制限を表示します)
                            """  # noqa: E501
                        ),
                        # "group": "group_a (required)",
                    },
                    {
                        "name": ["endpoint"],
                        "type": str,
                        "help": textwrap.dedent(
                            """\
                            - [グループA(必須)] エンドポイント
                                - 例："/friends/list"
                                - 例："" (両方とも空文字の場合は全てのレート制限を表示します)
                            """  # noqa: E501
                        ),
                        # "group": "group_a (required)",
                    },
                ],
            },
            {
                "name": ["search-tweet"],
                "help": DESC_OF_SEARCH_TWEET,
                "description": DESC_OF_SEARCH_TWEET,
                "func": twitter_tweet_search.search_twitter_tweet,
                "formatter_class": argparse.RawTextHelpFormatter,
                "arguments": [
                    # グループA(必須)
                    {
                        "name": ["query"],
                        "type": str,
                        "help": textwrap.dedent(
                            """\
                            - [グループA(必須)] クエリ
                                - RTと返信はデフォルトで除外します
                            """  # noqa: E501
                        ),
                        # "group": "group_a (required)",
                    },
                    # グループC(任意)
                    {
                        "name": ["-t", "--num_of_tweets"],
                        "type": int,
                        "default": 100,
                        "help": textwrap.dedent(
                            """\
                            - [グループC(任意)] ツイート数 (デフォルト：%(default)s)
                                - 表示するツイートの数
                                - 18000件を超過した場合はレート制限により18000件ごとに15分の待機時間が発生します
                            """  # noqa: E501
                        ),
                        # "group": "group_c (optional)",
                    },
                ],
            },
            {
                "name": ["stream-tweet"],
                "help": DESC_OF_STREAM_TWEET,
                "description": DESC_OF_STREAM_TWEET,
                "func": twitter_tweet_stream.stream_twitter_tweet,
                "formatter_class": argparse.RawTextHelpFormatter,
                "arguments": [
                    # グループB1(1つのみ必須)
                    {
                        "name": ["-ui", "--user_id_for_followees"],
                        "type": str,
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] ユーザID(フォロイー用)
                                - 指定したユーザIDのフォロイーのツイートを配信します
                            """  # noqa: E501
                        ),
                        "exclusive_group": "group_b1 (exclusive)",
                    },
                    {
                        "name": ["-li", "--list_id"],
                        "type": str,
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] リストID
                                - 指定したリストIDのツイートを配信します
                            """  # noqa: E501
                        ),
                        "exclusive_group": "group_b1 (exclusive)",
                    },
                    {
                        "name": ["-ln", "--list_name"],
                        "type": str,
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] リスト名
                                - 指定したリスト名のツイートを配信します
                            """  # noqa: E501
                        ),
                        "exclusive_group": "group_b1 (exclusive)",
                    },
                    {
                        "name": ["-fp", "--following_user_file_path"],
                        "type": str,
                        "nargs": 2,
                        "metavar": ("FILE_PATH", "HEADER_LINE_NUM"),
                        "help": textwrap.dedent(
                            """\
                            - [グループB1(1つのみ必須)] フォローユーザファイルパス(csvファイル) ヘッダ行番号
                                - 指定したファイルに記載されているユーザのツイートを配信します
                                - またヘッダ行番号は 0：ヘッダなし 1~：ヘッダとなるファイルの行番号 です
                            """  # noqa: E501
                        ),
                        "exclusive_group": "group_b1 (exclusive)",
                    },
                    # グループC(任意)
                    {
                        "name": ["-k", "--keyword_of_csv_format"],
                        "type": str,
                        "default": "",
                        "help": textwrap.dedent(
                            """\
                            - [グループC(任意)] キーワード(csv形式)
                                - 例："Google Docs, Google Drive"
                                - スペースはAND検索(Google AND Docs)
                                - カンマはOR検索(Google Docs OR Google Drive)
                            """  # noqa: E501
                        ),
                        # "group": "group_c (optional)",
                    },
                ],
            },
        ],
    },
}

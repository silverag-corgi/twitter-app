import argparse
import os
from typing import Optional

import python_lib_for_me as pyl


class TwitterApiBaseArg:
    """TwitterAPI基本引数"""

    def __init__(
        self,
        arg_namespace: argparse.Namespace,
    ) -> None:
        self.__use_debug_mode: bool = arg_namespace.use_debug_mode
        return None

    @property
    def use_debug_mode(self) -> bool:
        return self.__use_debug_mode


class TwitterApiAuthArg(TwitterApiBaseArg):
    """TwitterAPI認証引数"""

    def __init__(
        self,
        arg_namespace: argparse.Namespace,
    ) -> None:
        super().__init__(arg_namespace)

        # 引数検証
        self.__validate_arg()
        return None

    def __validate_arg(self) -> None:
        """引数検証"""

        clg: Optional[pyl.CustomLogger] = None

        try:
            # ロガーの取得
            clg = pyl.CustomLogger(__name__, use_debug_mode=self.use_debug_mode)

            # 引数指定の確認
            if self.__is_specified() is False:
                raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

            # 検証：なし
        except Exception as e:
            raise (e)

        return None

    def __is_specified(self) -> bool:
        """引数指定確認"""
        return True


class TwitterFollowxxExportArg(TwitterApiBaseArg):
    """Twitterフォロイー(フォロワー)エクスポート引数"""

    def __init__(
        self,
        arg_namespace: argparse.Namespace,
    ) -> None:
        super().__init__(arg_namespace)
        # グループA(必須)
        self.__user_id: str = arg_namespace.user_id
        # グループB1(1つのみ必須)
        self.__export_followee: bool = arg_namespace.export_followee
        self.__export_follower: bool = arg_namespace.export_follower
        # グループC(任意)
        self.__num_of_followxxs: int = arg_namespace.num_of_followxxs
        # 引数検証
        self.__validate_arg()
        return None

    def __validate_arg(self) -> None:
        """引数検証"""

        clg: Optional[pyl.CustomLogger] = None

        try:
            # ロガーの取得
            clg = pyl.CustomLogger(__name__, use_debug_mode=self.use_debug_mode)

            # 引数指定の確認
            if self.__is_specified() is False:
                raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

            # 検証：ユーザIDが4文字以上であること
            if not (len(self.user_id) >= 4):
                raise pyl.ArgumentValidationError(f"ユーザIDが4文字以上ではありません。(user_id:{self.user_id})")

            # 検証：フォロイー(フォロワー)数が1人以上であること
            if not (self.num_of_followxxs >= 1):
                raise pyl.ArgumentValidationError(
                    f"フォロイー(フォロワー)数が1人以上ではありません。(num_of_followxxs:{self.num_of_followxxs})"
                )
        except Exception as e:
            raise (e)

        return None

    def __is_specified(self) -> bool:
        """引数指定確認"""
        return (self.user_id is not None) and (
            self.export_followee is True or self.export_follower is True
        )

    @property
    def user_id(self) -> str:
        return self.__user_id

    @property
    def export_followee(self) -> bool:
        return self.__export_followee

    @property
    def export_follower(self) -> bool:
        return self.__export_follower

    @property
    def num_of_followxxs(self) -> int:
        return self.__num_of_followxxs


class TwitterListExportArg(TwitterApiBaseArg):
    """Twitterリストエクスポート引数"""

    def __init__(
        self,
        arg_namespace: argparse.Namespace,
    ) -> None:
        super().__init__(arg_namespace)
        # グループB1(1つのみ必須)
        self.__all_list: bool = arg_namespace.all_list
        self.__list_id: Optional[str] = arg_namespace.list_id
        self.__list_name: Optional[str] = arg_namespace.list_name
        # 引数検証
        self.__validate_arg()
        return None

    def __validate_arg(self) -> None:
        """引数検証"""

        clg: Optional[pyl.CustomLogger] = None

        try:
            # ロガーの取得
            clg = pyl.CustomLogger(__name__, use_debug_mode=self.use_debug_mode)

            # 引数指定の確認
            if self.__is_specified() is False:
                raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

            # 検証：グループBの引数が指定された場合は1文字以上であること
            if self.list_id is not None and not (len(self.list_id) >= 1):
                raise pyl.ArgumentValidationError(f"リストIDが1文字以上ではありません。(list_id:{self.list_id})")
            elif self.list_name is not None and not (len(self.list_name) >= 1):
                raise pyl.ArgumentValidationError(f"リスト名が1文字以上ではありません。(list_name:{self.list_name})")
        except Exception as e:
            raise (e)

        return None

    def __is_specified(self) -> bool:
        """引数指定確認"""
        return self.__all_list is True or self.__list_id is not None or self.__list_name is not None

    @property
    def all_list(self) -> bool:
        return self.__all_list

    @property
    def list_id(self) -> Optional[str]:
        return self.__list_id

    @property
    def list_name(self) -> Optional[str]:
        return self.__list_name


class TwitterListImportArg(TwitterApiBaseArg):
    """Twitterリストインポート引数"""

    def __init__(
        self,
        arg_namespace: argparse.Namespace,
    ) -> None:
        super().__init__(arg_namespace)
        # グループC(任意)
        self.__list_member_file_path: str = arg_namespace.list_member_file_path
        self.__header_line_num: int = arg_namespace.header_line_num
        self.__add_only_users_with_diff: bool = arg_namespace.add_only_users_with_diff
        # 引数検証
        self.__validate_arg()
        return None

    def __validate_arg(self) -> None:
        """引数検証"""

        clg: Optional[pyl.CustomLogger] = None

        try:
            # ロガーの取得
            clg = pyl.CustomLogger(__name__, use_debug_mode=self.use_debug_mode)

            # 引数指定の確認
            if self.__is_specified() is False:
                raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

            # 検証：リストメンバーファイルパスがcsvファイルのパスであること
            list_member_file_path_and_ext: tuple[str, str] = os.path.splitext(
                self.list_member_file_path
            )
            if not (list_member_file_path_and_ext[1] == ".csv"):
                raise pyl.ArgumentValidationError(
                    f"リストメンバーファイルパスがcsvファイルのパスではありません。(list_member_file_path:{self.list_member_file_path})"
                )

            # 検証：ヘッダ行番号が0以上であること
            if not (self.header_line_num >= 0):
                raise pyl.ArgumentValidationError(
                    f"ヘッダ行番号が0以上ではありません。(header_line_num:{self.header_line_num})"
                )
        except Exception as e:
            raise (e)

        return None

    def __is_specified(self) -> bool:
        """引数指定確認"""
        return True

    @property
    def list_member_file_path(self) -> str:
        return self.__list_member_file_path

    @property
    def header_line_num(self) -> int:
        return self.__header_line_num

    @property
    def add_only_users_with_diff(self) -> bool:
        return self.__add_only_users_with_diff


class TwitterListShowArg(TwitterApiBaseArg):
    """Twitterリスト表示引数"""

    def __init__(
        self,
        arg_namespace: argparse.Namespace,
    ) -> None:
        super().__init__(arg_namespace)
        # グループB1(1つのみ必須)
        self.__all_list: bool = arg_namespace.all_list
        self.__list_id: Optional[str] = arg_namespace.list_id
        self.__list_name: Optional[str] = arg_namespace.list_name
        # 引数検証
        self.__validate_arg()
        return None

    def __validate_arg(self) -> None:
        """引数検証"""

        clg: Optional[pyl.CustomLogger] = None

        try:
            # ロガーの取得
            clg = pyl.CustomLogger(__name__, use_debug_mode=self.use_debug_mode)

            # 引数指定の確認
            if self.__is_specified() is False:
                raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

            # 検証：グループBの引数が指定された場合は1文字以上であること
            if self.list_id is not None and not (len(self.list_id) >= 1):
                raise pyl.ArgumentValidationError(f"リストIDが1文字以上ではありません。(list_id:{self.list_id})")
            elif self.list_name is not None and not (len(self.list_name) >= 1):
                raise pyl.ArgumentValidationError(f"リスト名が1文字以上ではありません。(list_name:{self.list_name})")
        except Exception as e:
            raise (e)

        return None

    def __is_specified(self) -> bool:
        """引数指定確認"""
        return self.__all_list is True or self.__list_id is not None or self.__list_name is not None

    @property
    def all_list(self) -> bool:
        return self.__all_list

    @property
    def list_id(self) -> Optional[str]:
        return self.__list_id

    @property
    def list_name(self) -> Optional[str]:
        return self.__list_name


class TwitterRateLimitShowArg(TwitterApiBaseArg):
    """Twitterレート制限表示引数"""

    def __init__(
        self,
        arg_namespace: argparse.Namespace,
    ) -> None:
        super().__init__(arg_namespace)
        # グループA(必須)
        self.__resource_family: str = arg_namespace.resource_family
        self.__endpoint: str = arg_namespace.endpoint
        # 引数検証
        self.__validate_arg()
        return None

    def __validate_arg(self) -> None:
        """引数検証"""

        clg: Optional[pyl.CustomLogger] = None

        try:
            # ロガーの取得
            clg = pyl.CustomLogger(__name__, use_debug_mode=self.use_debug_mode)

            # 引数指定の確認
            if self.__is_specified() is False:
                raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

            # 検証：なし
        except Exception as e:
            raise (e)

        return None

    def __is_specified(self) -> bool:
        """引数指定確認"""
        return self.__resource_family is not None and self.__endpoint is not None

    @property
    def resource_family(self) -> str:
        return self.__resource_family

    @property
    def endpoint(self) -> str:
        return self.__endpoint


class TwitterTweetSearchArg(TwitterApiBaseArg):
    """Twitterツイート検索引数"""

    def __init__(
        self,
        arg_namespace: argparse.Namespace,
    ) -> None:
        super().__init__(arg_namespace)
        # グループA(必須)
        self.__query: str = arg_namespace.query
        # グループC(任意)
        self.__num_of_tweets: int = arg_namespace.num_of_tweets
        # 引数検証
        self.__validate_arg()
        return None

    def __validate_arg(self) -> None:
        """引数検証"""

        clg: Optional[pyl.CustomLogger] = None

        try:
            # ロガーの取得
            clg = pyl.CustomLogger(__name__, use_debug_mode=self.use_debug_mode)

            # 引数指定の確認
            if self.__is_specified() is False:
                raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

            # 検証：クエリが1文字以上であること
            if not (len(self.query) >= 1):
                raise pyl.ArgumentValidationError(f"クエリが1文字以上ではありません。(query:{self.query})")

            # 検証：ツイート数が1件以上であること
            if not (self.num_of_tweets >= 1):
                raise pyl.ArgumentValidationError(
                    f"ツイート数が1件以上ではありません。(num_of_tweets:{self.num_of_tweets})"
                )
        except Exception as e:
            raise (e)

        return None

    def __is_specified(self) -> bool:
        """引数指定確認"""
        return self.__query is not None

    @property
    def query(self) -> str:
        return self.__query

    @property
    def num_of_tweets(self) -> int:
        return self.__num_of_tweets


class TwitterTweetStreamArg(TwitterApiBaseArg):
    """Twitterツイート配信引数"""

    def __init__(
        self,
        arg_namespace: argparse.Namespace,
    ) -> None:
        super().__init__(arg_namespace)
        # グループB1(1つのみ必須)
        self.__user_id_for_followees: Optional[str] = arg_namespace.user_id_for_followees
        self.__list_id: Optional[str] = arg_namespace.list_id
        self.__list_name: Optional[str] = arg_namespace.list_name
        self.__following_user_file_path: Optional[list] = arg_namespace.following_user_file_path
        # グループC(任意)
        self.__keyword_of_csv_format: str = arg_namespace.keyword_of_csv_format
        # 引数検証
        self.__validate_arg()
        return None

    def __validate_arg(self) -> None:
        """引数検証"""

        clg: Optional[pyl.CustomLogger] = None

        try:
            # ロガーの取得
            clg = pyl.CustomLogger(__name__, use_debug_mode=self.use_debug_mode)

            # 引数指定の確認
            if self.__is_specified() is False:
                raise pyl.ArgumentValidationError(f"サブコマンドの引数が指定されていません。")

            # 検証：グループAの引数が指定された場合は1文字以上であること
            if self.user_id_for_followees is not None and not (
                len(self.user_id_for_followees) >= 1
            ):
                raise pyl.ArgumentValidationError(
                    f"ユーザID(フォロイー用)が1文字以上ではありません。(user_id_for_followees:{self.user_id_for_followees})",
                )
            elif self.list_id is not None and not (len(self.list_id) >= 1):
                raise pyl.ArgumentValidationError(f"リストIDが1文字以上ではありません。(list_id:{self.list_id})")
            elif self.list_name is not None and not (len(self.list_name) >= 1):
                raise pyl.ArgumentValidationError(f"リスト名が1文字以上ではありません。(list_name:{self.list_name})")
            elif self.following_user_file_path is not None and not (
                len(self.following_user_file_path[0]) >= 1
            ):
                raise pyl.ArgumentValidationError(
                    f"フォローユーザファイルパスが1文字以上ではありません。(following_user_file_path[0]:{self.following_user_file_path[0]})",
                )

            # 検証：フォローユーザファイルパスがcsvファイルのパスであること
            if self.following_user_file_path is not None and not (
                os.path.splitext(self.following_user_file_path[0])[1] == ".csv"
            ):
                raise pyl.ArgumentValidationError(
                    f"フォローユーザファイルパスがcsvファイルのパスではありません。(following_user_file_path[0]:{self.following_user_file_path[0]})",
                )

            # 検証：フォローユーザファイルパスのファイルが存在すること
            if self.following_user_file_path is not None and not (
                os.path.isfile(self.following_user_file_path[0]) is True
            ):
                raise pyl.ArgumentValidationError(
                    f"フォローユーザファイルパスのファイルが存在しません。(following_user_file_path[0]:{self.following_user_file_path[0]})",
                )

            # 検証：ヘッダ行番号が0以上であること
            if self.following_user_file_path is not None and not (
                str(self.following_user_file_path[1]).isdecimal() is True
            ):
                raise pyl.ArgumentValidationError(
                    f"ヘッダ行番号が0以上ではありません。(following_user_file_path[1]:{self.following_user_file_path[1]})",
                )
        except Exception as e:
            raise (e)

        return None

    def __is_specified(self) -> bool:
        """引数指定確認"""
        return (
            self.__user_id_for_followees is not None
            or self.__list_id is not None
            or self.__list_name is not None
            or self.__following_user_file_path is not None
        )

    @property
    def user_id_for_followees(self) -> Optional[str]:
        return self.__user_id_for_followees

    @property
    def list_id(self) -> Optional[str]:
        return self.__list_id

    @property
    def list_name(self) -> Optional[str]:
        return self.__list_name

    @property
    def following_user_file_path(self) -> Optional[list]:
        return self.__following_user_file_path

    @property
    def keyword_of_csv_format(self) -> str:
        return self.__keyword_of_csv_format

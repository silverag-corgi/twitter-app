import argparse
from typing import Optional


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
        return None

    def is_specified(self) -> bool:
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
        return None

    def is_specified(self) -> bool:
        return (self.__user_id is not None) and (
            self.__export_followee is True or self.__export_follower is True
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
        return None

    def is_specified(self) -> bool:
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
        return None

    def is_specified(self) -> bool:
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
        return None

    def is_specified(self) -> bool:
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
        return None

    def is_specified(self) -> bool:
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
        return None

    def is_specified(self) -> bool:
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
        return None

    def is_specified(self) -> bool:
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

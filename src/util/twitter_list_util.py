import tweepy


def has_twitter_list(api: tweepy.API, list_name: str) -> bool:
    '''Twitterリスト存在確認'''

    twitter_lists: list[tweepy.List] = api.get_lists()
    for twitter_list in twitter_lists:
        if twitter_list.name == list_name:
            print(f'Twitterリストが既に存在します。(リスト名：{twitter_list.name})')
            return True

    return False


def generate_twitter_list(api: tweepy.API, twitter_list_name: str) -> tweepy.List:
    '''Twitterリスト作成'''

    try:
        twitter_list: tweepy.List = api.create_list(twitter_list_name, mode='private', description='')
        print(f'Twitterリスト作成に成功しました。(リスト名：{twitter_list.name})')
    except Exception as e:
        print(f'Twitterリスト作成に失敗しました。')
        raise(e)

    return twitter_list


def add_user(api: tweepy.API, twitter_list: tweepy.List, user_id: str, user_name: str) -> None:
    '''ユーザ追加'''

    try:
        api.add_list_member(list_id=twitter_list.id, screen_name=user_id)
        print(f'ユーザ追加に成功しました。(ユーザID：{user_id: <20}、ユーザ名：{user_name})')
    except Exception as e:
        # ユーザが鍵付きや削除済みなどの場合
        print(f'ユーザ追加に失敗しました。(ユーザID：{user_id: <20}、ユーザ名：{user_name})')

    return None

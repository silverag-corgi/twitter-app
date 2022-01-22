import sys
import traceback

from src import api_auth, twitter_list_gen


def main():
    try:
        # Twitter認証実行
        api = api_auth.main()

        # Twitterリスト作成
        twitter_list_gen.main(api)
    except Exception as e:
        print(traceback.format_exc())
        return 1
    
    return 0


sys.exit(main())

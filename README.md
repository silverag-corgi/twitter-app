# twitter-app <!-- omit in toc -->

## 0. 目次 <!-- omit in toc -->

- [1. 概要](#1-概要)
- [2. 機能](#2-機能)
- [3. 動作確認済み環境](#3-動作確認済み環境)
- [4. 事前準備](#4-事前準備)
  - [4.1. TwitterAPI認証情報の発行](#41-twitterapi認証情報の発行)
    - [4.1.1. (A)Twitter開発者ポータルサイトで申請する手順](#411-atwitter開発者ポータルサイトで申請する手順)
    - [4.1.2. (B)Twitter社が公開しているコンシューマーキーとPINコードにより発行する手順](#412-btwitter社が公開しているコンシューマーキーとpinコードにより発行する手順)
- [5. セットアップ手順](#5-セットアップ手順)
  - [5.1. リポジトリのクローン](#51-リポジトリのクローン)
  - [5.2. 仮想環境の構築](#52-仮想環境の構築)
  - [5.3. TwitterAPI認証情報の設定](#53-twitterapi認証情報の設定)
- [6. 使い方](#6-使い方)
  - [6.1. メインコマンド](#61-メインコマンド)
    - [6.1.1. ヘルプ](#611-ヘルプ)
  - [6.2. サブコマンド：TwitterAPI認証](#62-サブコマンドtwitterapi認証)
    - [6.2.1. ヘルプ](#621-ヘルプ)
    - [6.2.2. 実行結果](#622-実行結果)
      - [6.2.2.1. TwitterAPI認証情報ファイル](#6221-twitterapi認証情報ファイル)
  - [6.3. サブコマンド：Twitterフォロイー(フォロワー)エクスポート](#63-サブコマンドtwitterフォロイーフォロワーエクスポート)
    - [6.3.1. ヘルプ](#631-ヘルプ)
    - [6.3.2. 実行結果](#632-実行結果)
      - [6.3.2.1. フォロイーファイル](#6321-フォロイーファイル)
      - [6.3.2.2. フォロワーファイル](#6322-フォロワーファイル)
  - [6.4. サブコマンド：Twitterリストエクスポート](#64-サブコマンドtwitterリストエクスポート)
    - [6.4.1. ヘルプ](#641-ヘルプ)
    - [6.4.2. 実行結果](#642-実行結果)
      - [6.4.2.1. リストメンバーファイル](#6421-リストメンバーファイル)
  - [6.5. サブコマンド：Twitterリストインポート](#65-サブコマンドtwitterリストインポート)
    - [6.5.1. 事前準備：リストメンバーファイルの作成](#651-事前準備リストメンバーファイルの作成)
    - [6.5.2. ヘルプ](#652-ヘルプ)
    - [6.5.3. 実行結果](#653-実行結果)
      - [6.5.3.1. Twitterリスト](#6531-twitterリスト)
  - [6.6. サブコマンド：Twitterリスト表示](#66-サブコマンドtwitterリスト表示)
    - [6.6.1. ヘルプ](#661-ヘルプ)
    - [6.6.2. 実行結果](#662-実行結果)
      - [6.6.2.1. Twitterリスト一覧](#6621-twitterリスト一覧)
  - [6.7. サブコマンド：Twitterレート制限表示](#67-サブコマンドtwitterレート制限表示)
    - [6.7.1. ヘルプ](#671-ヘルプ)
    - [6.7.2. 実行結果](#672-実行結果)
      - [6.7.2.1. Twitterレート制限](#6721-twitterレート制限)
  - [6.8. サブコマンド：Twitterツイート検索](#68-サブコマンドtwitterツイート検索)
    - [6.8.1. ヘルプ](#681-ヘルプ)
    - [6.8.2. 実行結果](#682-実行結果)
      - [6.8.2.1. ツイート検索結果ファイル](#6821-ツイート検索結果ファイル)
  - [6.9. サブコマンド：Twitterツイート配信](#69-サブコマンドtwitterツイート配信)
    - [6.9.1. ヘルプ](#691-ヘルプ)
    - [6.9.2. 実行結果](#692-実行結果)
      - [6.9.2.1. Twitterツイート](#6921-twitterツイート)
- [7. 連絡先](#7-連絡先)
- [8. ライセンス](#8-ライセンス)

## 1. 概要

TwitterAPIを利用したアプリケーション。

## 2. 機能

アプリケーションとしてコマンドラインから実行できる。

- TwitterAPI認証
  - コンシューマーキーとPINコードを基にアクセストークンを生成し、認証情報ファイルに保存する
- Twitterフォロイー(フォロワー)エクスポート
  - 指定したユーザのフォロイー(フォロワー)をエクスポートする
- Twitterリストエクスポート
  - 指定したリストをTwitterからエクスポートする
- Twitterリストインポート
  - 指定したcsvファイルをリストとしてTwitterにインポートする
- Twitterリスト表示
  - 指定したリストを表示する
- Twitterレート制限表示
  - 指定したリソース群とエンドポイントのレート制限を表示する
- Twitterツイート検索
  - 指定したクエリでツイートを検索し、ツイート検索結果ファイルを生成する
- Twitterツイート配信
  - 指定したキーワードのツイートを配信する

## 3. 動作確認済み環境

- Debian 11
- [Python 3.10.1](https://www.python.org/downloads/release/python-3101/)
- [Poetry 1.1.12](https://python-poetry.org/docs/#installing-with-pip)

## 4. 事前準備

### 4.1. TwitterAPI認証情報の発行

認証情報を発行する手順は、以下の通り2種類ある。

- (A)Twitter開発者ポータルサイトで申請する手順
- (B)Twitter社が公開しているコンシューマーキーとPINコードにより発行する手順

Bの手順は5分程度で完了するが、Twitter社が突然公開を停止する可能性があるため、
いつの間にか認証できなくなるということが起こり得る。
そのため、試しに手早く動かしてみたい方向けである。

それに対してAの手順は2～3時間＋申請待ち時間を必要とするが、
ポータルサイトで発行するため自身で認証情報を破棄しない限り、
認証できなくなるということは起こり得ない。
そのため、開発者などの長期的に使用する方向けである。

#### 4.1.1. (A)Twitter開発者ポータルサイトで申請する手順

[Twitter Developer Portal](https://developer.twitter.com/en/apply-for-access)
で認証情報を発行する。

発行手順は長くなる上に頻繁に仕様が変更されるため
[ググる](https://www.google.com/search?q=TwitterAPI+申請+解説)
こと。
2022年3月時点では
[Twitter APIの申請方法を解説【2022年版】](https://mitchieblog.com/twitter-api-apply/)
を参考に申請するとよい。

また、以下の通り設定する。

|  No | 設定項目                                       | 設定値                            | 備考   |
| --: | ---------------------------------------------- | --------------------------------- | ------ |
|  01 | User authentication settings - Methods         | OAuth 1.0a                        |        |
|  02 | User authentication settings - App permissions | Read and write and Direct message |        |
|  03 | Consumer Keys - API Key                        | (自動生成値)                      | (1)    |
|  04 | Consumer Keys - API Secret                     | (自動生成値)                      | (1)    |
|  05 | Authentication Tokens - Access Token           | (自動生成値)                      | (2)(3) |
|  06 | Authentication Tokens - Access Token Secret    | (自動生成値)                      | (2)(3) |
|  07 | Access levels                                  | Elevated                          | (4)    |

(1)アプリの認証情報。アプリとは、Twitterクライアント(TweetDeckなど)やTwitter管理ツール(SocialDogなど)のこと。

(2)ユーザの認証情報。ユーザとは、Twitterアカウントのこと。

(3)`App permissions`を変更した場合は再生成する必要がある。

(4)`Twitter API v1.1`を使用するため、`Essential`からのアップグレードを申請する必要がある。

#### 4.1.2. (B)Twitter社が公開しているコンシューマーキーとPINコードにより発行する手順

[Twitter Official/unOfficial Credentials - Twitter for Mac](https://gist.github.com/shobotch/5160017#twitter-for-mac)
に掲載されている下記項目を利用する。

- Consumer Key = API Key
- Consumer Secret = API Secret

ここで本項は一旦保留する。

[5.2. 仮想環境の構築](#52-仮想環境の構築)
まで完了した後に、上記項目を用いて
[5.3. TwitterAPI認証情報の設定](#53-twitterapi認証情報の設定)
及び
[6.2. サブコマンド：TwitterAPI認証](#62-サブコマンドtwitterapi認証)
を実行する。

## 5. セットアップ手順

前提として、PythonとPoetryがインストール済みであること。

### 5.1. リポジトリのクローン

下記リポジトリをクローンもしくはダウンロードする。

- twitter-app
  - 本リポジトリ
- python-lib-for-me
  - 自分用のPythonライブラリ

### 5.2. 仮想環境の構築

下記コマンドを実行する。

```shell
$ cd twitter-app                            # アプリケーションのパスに移動する
$ poetry config virtualenvs.in-project true # 仮想環境のインストール先をプロジェクト配下に設定する
$ poetry install                            # pyproject.tomlを基に仮想環境をインストールする
```

そして、下記コマンドを実行して、アプリケーション配下に`.venv`フォルダが作成されていることを確認する。

```shell
$ poetry env info --path                    # 仮想環境のインストール先を表示する
/root/workspace/Git/python/twitter-app/.venv
```

### 5.3. TwitterAPI認証情報の設定

`config/twitter_api_auth_info.json.sample`をコピペし、拡張子`.sample`を削除し、発行した認証情報を保存する。

```shell
$ cat config/twitter_api_auth_info.json
{
  "consumer_keys": {
    "api_key"             : "xxxxx",
    "api_secret"          : "xxxxx"
  },
  "authentication_tokens": {
    "bearer_token"        : "xxxxx",
    "access_token"        : "xxxxx",
    "access_token_secret" : "xxxxx"
  }
}
```

## 6. 使い方

アプリケーションの実行手順を機能ごとに示す。

### 6.1. メインコマンド

#### 6.1.1. ヘルプ

下記コマンドでヘルプを呼び出す。

```shell
$ poetry run twitter -h
[INF][         MainProcess][          MainThread][                                 main.py:0021][                                    main] コマンド：['twitter', '-h']
[INF][         MainProcess][          MainThread][                           arg_parser.py:0046][                          _print_message] 
usage: twitter [-h] [-d] {auth-api,exp-followxx,exp-list,imp-list,show-list,show-limit,search-tweet,stream-tweet} ...

twitter-app
TwitterAPIを利用したアプリケーション。

options:
  -h, --help            show this help message and exit
  -d, --use_debug_mode  デバッグモード使用有無

sub_commands:
  {auth-api,exp-followxx,exp-list,imp-list,show-list,show-limit,search-tweet,stream-tweet}
    auth-api            - 機能名
                            - TwitterAPI認証
                        - 概要
                            - コンシューマーキーとPINコードを基にアクセストークンを生成し、認証情報ファイルに保存します
                        - 生成ファイル
                            - TwitterAPI認証情報ファイル
                                - config/twitter_api_auth_info.json
                        - コマンド例
                            - poetry run twitter auth-api
    exp-followxx        - 機能名
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
    exp-list            - 機能名
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
    imp-list            - 機能名
                            - Twitterリストインポート
                        - 概要
                            - 指定したcsvファイルをリストとしてTwitterにインポートします
                        - コマンド例
                            - poetry run twitter imp-list -l "input/list_member/*.csv" -hd 1 -d
    show-list           - 機能名
                            - Twitterリスト表示
                        - 概要
                            - 指定したリストを表示します
                        - コマンド例
                            - poetry run twitter show-list -all
                            - poetry run twitter show-list -id "0123456789111111111, 0123456789222222222"
                            - poetry run twitter show-list -name "Google関連, Microsoft関連"
    show-limit          - 機能名
                            - Twitterレート制限表示
                        - 概要
                            - 指定したリソース群とエンドポイントのレート制限を表示します
                        - コマンド例
                            - poetry run twitter show-limit "friends" "/friends/list"
                            - poetry run twitter show-limit "" ""
    search-tweet        - 機能名
                            - Twitterツイート検索
                        - 概要
                            - 指定したクエリでツイートを検索し、ツイート検索結果ファイルを生成します
                        - 生成ファイル
                            - ツイート検索結果ファイル
                                - ./dest/tweet_search_result/[クエリ].csv
                        - コマンド例
                            - poetry run twitter search-tweet "API" -t 100
    stream-tweet        - 機能名
                            - Twitterツイート配信
                        - 概要
                            - 指定したキーワードのツイートを配信します
                        - コマンド例
                            - poetry run twitter stream-tweet -ui "silverag_corgi" -k "Google Docs, Google Drive"
                            - poetry run twitter stream-tweet -li "0123456789111111111" -k "Google Docs, Google Drive"
                            - poetry run twitter stream-tweet -ln "Google関連" -k "Google Docs, Google Drive"
                            - poetry run twitter stream-tweet -fp "input/list_member/*.csv" 1 -k "Google Docs, Google Drive"
```

### 6.2. サブコマンド：TwitterAPI認証

[4.1.2. (B)Twitter社が公開しているコンシューマーキーとPINコードにより発行する手順](#412-btwitter社が公開しているコンシューマーキーとpinコードにより発行する手順)
を選択した場合に実行する必要がある。

#### 6.2.1. ヘルプ

下記コマンドでヘルプを呼び出す。

```shell
$ poetry run twitter auth-api -h
[INF][         MainProcess][          MainThread][                                 main.py:0021][                                    main] コマンド：['twitter', 'auth-api', '-h']
[INF][         MainProcess][          MainThread][                           arg_parser.py:0046][                          _print_message] 
usage: twitter auth-api [-h]

- 機能名
    - TwitterAPI認証
- 概要
    - コンシューマーキーとPINコードを基にアクセストークンを生成し、認証情報ファイルに保存します
- 生成ファイル
    - TwitterAPI認証情報ファイル
        - config/twitter_api_auth_info.json
- コマンド例
    - poetry run twitter auth-api

options:
  -h, --help  show this help message and exit
```

#### 6.2.2. 実行結果

アクセストークンが生成され、TwitterAPI認証情報ファイルに追記される。

##### 6.2.2.1. TwitterAPI認証情報ファイル

例として下記コマンドを実行する。

```shell
$ poetry run pin-auth
```

実行することにより、ファイルが下記パスに生成される。

| 種類         | ファイルパス                      |
| ------------ | --------------------------------- |
| フォーマット | config/twitter_api_auth_info.json |
| 例           | config/twitter_api_auth_info.json |

### 6.3. サブコマンド：Twitterフォロイー(フォロワー)エクスポート

#### 6.3.1. ヘルプ

下記コマンドでヘルプを呼び出す。

```shell
$ poetry run twitter exp-followxx -h
[INF][         MainProcess][          MainThread][                                 main.py:0021][                                    main] コマンド：['twitter', 'exp-followxx', '-h']
[INF][         MainProcess][          MainThread][                           arg_parser.py:0046][                          _print_message] 
usage: twitter exp-followxx [-h] [-e | -r] [-f NUM_OF_FOLLOWXXS] user_id

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

positional arguments:
  user_id               - [グループA(必須)] ユーザID

options:
  -h, --help            show this help message and exit
  -e, --export_followee
                        - [グループB1(1つのみ必須)] フォロイーエクスポート要否
                            - フォロイー(指定したユーザがフォローしているユーザ)をエクスポートします
  -r, --export_follower
                        - [グループB1(1つのみ必須)] フォロワーエクスポート要否
                            - フォロワー(指定したユーザをフォローしているユーザ)をエクスポートします
  -f NUM_OF_FOLLOWXXS, --num_of_followxxs NUM_OF_FOLLOWXXS
                        - [グループC(任意)] フォロイー(フォロワー)数 (デフォルト：3000)
                            - エクスポートするフォロイー(フォロワー)の人数
                            - 3000人を超過した場合はレート制限により3000人ごとに15分の待機時間が発生します
```

#### 6.3.2. 実行結果

フォロイー(フォロワー)ファイルが生成される。

##### 6.3.2.1. フォロイーファイル

例として下記コマンドを実行する。

```shell
$ poetry run twitter exp-followxx "silverag_corgi" -e -f 3000
```

実行することにより、ファイルが下記パスに生成される。

| 種類         | ファイルパス                       |
| ------------ | ---------------------------------- |
| フォーマット | ./dest/followee/[ユーザID].csv     |
| 例           | ./dest/followee/silverag_corgi.csv |

##### 6.3.2.2. フォロワーファイル

例として下記コマンドを実行する。

```shell
$ poetry run twitter exp-followxx "silverag_corgi" -r -f 3000
```

実行することにより、ファイルが下記パスに生成される。

| 種類         | ファイルパス                       |
| ------------ | ---------------------------------- |
| フォーマット | ./dest/follower/[ユーザID].csv     |
| 例           | ./dest/follower/silverag_corgi.csv |

### 6.4. サブコマンド：Twitterリストエクスポート

#### 6.4.1. ヘルプ

下記コマンドでヘルプを呼び出す。

```shell
$ poetry run twitter exp-list -h
[INF][         MainProcess][          MainThread][                                 main.py:0021][                                    main] コマンド：['twitter', 'exp-list', '-h']
[INF][         MainProcess][          MainThread][                           arg_parser.py:0046][                          _print_message] 
usage: twitter exp-list [-h] [-all | -id LIST_ID | -name LIST_NAME]

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

options:
  -h, --help            show this help message and exit
  -all, --all_list      - [グループB1(1つのみ必須)] 全てのリスト
  -id LIST_ID, --list_id LIST_ID
                        - [グループB1(1つのみ必須)] リストID(csv形式)
                            - 例："0123456789111111111, 0123456789222222222"
  -name LIST_NAME, --list_name LIST_NAME
                        - [グループB1(1つのみ必須)] リスト名(csv形式)
                            - 例："Google関連, Microsoft関連"
```

#### 6.4.2. 実行結果

リストメンバーファイルが生成される。

##### 6.4.2.1. リストメンバーファイル

例として下記コマンドを実行する。

```shell
$ poetry run twitter exp-list -all
$ poetry run twitter exp-list -id "0123456789111111111, 0123456789222222222"
$ poetry run twitter exp-list -name "Google関連, Microsoft関連"
```

実行することにより、ファイルが下記パスに生成される。

| 種類         | ファイルパス                      |
| ------------ | --------------------------------- |
| フォーマット | ./dest/list_member/[リスト名].csv |
| 例           | ./dest/list_member/Google関連.csv |

### 6.5. サブコマンド：Twitterリストインポート

#### 6.5.1. 事前準備：リストメンバーファイルの作成

1. リストメンバーサンプルファイル`input/list_member.csv.sample`をコピペする
2. 拡張子`.sample`を削除する
3. 作成したいリスト名にリネームする
4. csv形式でリストに追加したいユーザ(ユーザID、ユーザ名)を記入する

```shell
$ cat list_member.csv.sample
user_id,user_name
googledocs,Google Docs
googledrive,Google Drive
googlemaps,Google Maps
```

また、前述の
[6.3. サブコマンド：Twitterフォロイー(フォロワー)エクスポート](#63-サブコマンドtwitterフォロイーフォロワーエクスポート)
及び
[6.4. サブコマンド：Twitterリストエクスポート](#64-サブコマンドtwitterリストエクスポート)
の出力ファイルがリストメンバーファイルであるため、入力ファイルになる。

#### 6.5.2. ヘルプ

下記コマンドでヘルプを呼び出す。

```shell
$ poetry run twitter imp-list -h
[INF][         MainProcess][          MainThread][                                 main.py:0021][                                    main] コマンド：['twitter', 'imp-list', '-h']
[INF][         MainProcess][          MainThread][                           arg_parser.py:0046][                          _print_message] 
usage: twitter imp-list [-h] [-l LIST_MEMBER_FILE_PATH] [-hd HEADER_LINE_NUM] [-d]

- 機能名
    - Twitterリストインポート
- 概要
    - 指定したcsvファイルをリストとしてTwitterにインポートします
- コマンド例
    - poetry run twitter imp-list -l "input/list_member/*.csv" -hd 1 -d

options:
  -h, --help            show this help message and exit
  -l LIST_MEMBER_FILE_PATH, --list_member_file_path LIST_MEMBER_FILE_PATH
                        - [グループC(任意)] リストメンバーファイルパス(csvファイル) (デフォルト：input/list_member/*.csv)
                            - ワイルドカード可
  -hd HEADER_LINE_NUM, --header_line_num HEADER_LINE_NUM
                        - [グループC(任意)] ヘッダ行番号 (デフォルト：1)
                            - 0：ヘッダなし
                            - 1~：ヘッダとなるファイルの行番号
  -d, --add_only_users_with_diff
                        - [グループC(任意)] 差分ユーザ追加
                            - 指定した場合は既存のリストに差分のあるユーザのみを追加します
                            - 指定しない場合は既存のリストを削除して新しいリストにユーザを追加します
```

#### 6.5.3. 実行結果

Twitterにリストが生成される。

##### 6.5.3.1. Twitterリスト

例として下記コマンドを実行する。

```shell
$ poetry run twitter imp-list -l "input/list_member/*.csv" -hd 1 -d
```

### 6.6. サブコマンド：Twitterリスト表示

#### 6.6.1. ヘルプ

下記コマンドでヘルプを呼び出す。

```shell
$ poetry run twitter show-list -h
[INF][         MainProcess][          MainThread][                                 main.py:0021][                                    main] コマンド：['twitter', 'show-list', '-h']
[INF][         MainProcess][          MainThread][                           arg_parser.py:0046][                          _print_message] 
usage: twitter show-list [-h] [-all | -id LIST_ID | -name LIST_NAME]

- 機能名
    - Twitterリスト表示
- 概要
    - 指定したリストを表示します
- コマンド例
    - poetry run twitter show-list -all
    - poetry run twitter show-list -id "0123456789111111111, 0123456789222222222"
    - poetry run twitter show-list -name "Google関連, Microsoft関連"

options:
  -h, --help            show this help message and exit
  -all, --all_list      - [グループB1(1つのみ必須)] 全てのリスト
  -id LIST_ID, --list_id LIST_ID
                        - [グループB1(1つのみ必須)] リストID(csv形式)
                            - 例："0123456789111111111, 0123456789222222222"
  -name LIST_NAME, --list_name LIST_NAME
                        - [グループB1(1つのみ必須)] リスト名(csv形式)
                            - 例："Google関連, Microsoft関連"
```

#### 6.6.2. 実行結果

Twitterリストの一覧が表示される。

##### 6.6.2.1. Twitterリスト一覧

例として下記コマンドを実行する。

```shell
$ poetry run twitter show-list -all
$ poetry run twitter show-list -id "0123456789111111111, 0123456789222222222"
$ poetry run twitter show-list -name "Google関連, Microsoft関連"
```

### 6.7. サブコマンド：Twitterレート制限表示

#### 6.7.1. ヘルプ

下記コマンドでヘルプを呼び出す。

```shell
$ poetry run twitter show-limit -h
[INF][         MainProcess][          MainThread][                                 main.py:0021][                                    main] コマンド：['twitter', 'show-limit', '-h']
[INF][         MainProcess][          MainThread][                           arg_parser.py:0046][                          _print_message] 
usage: twitter show-limit [-h] resource_family endpoint

- 機能名
    - Twitterレート制限表示
- 概要
    - 指定したリソース群とエンドポイントのレート制限を表示します
- コマンド例
    - poetry run twitter show-limit "friends" "/friends/list"
    - poetry run twitter show-limit "" ""

positional arguments:
  resource_family  - [グループA(必須)] リソース群
                       - 例："friends"
                       - 例："" (両方とも空文字の場合は全てのレート制限を表示します)
  endpoint         - [グループA(必須)] エンドポイント
                       - 例："/friends/list"
                       - 例："" (両方とも空文字の場合は全てのレート制限を表示します)

options:
  -h, --help       show this help message and exit
```

#### 6.7.2. 実行結果

Twitterレート制限が表示される。

##### 6.7.2.1. Twitterレート制限

例として下記コマンドを実行する。

```shell
$ poetry run twitter show-limit "friends" "/friends/list"
$ poetry run twitter show-limit "" ""
```

### 6.8. サブコマンド：Twitterツイート検索

#### 6.8.1. ヘルプ

下記コマンドでヘルプを呼び出す。

```shell
$ poetry run twitter search-tweet -h
[INF][         MainProcess][          MainThread][                                 main.py:0021][                                    main] コマンド：['twitter', 'search-tweet', '-h']
[INF][         MainProcess][          MainThread][                           arg_parser.py:0046][                          _print_message] 
usage: twitter search-tweet [-h] [-t NUM_OF_TWEETS] query

- 機能名
    - Twitterツイート検索
- 概要
    - 指定したクエリでツイートを検索し、ツイート検索結果ファイルを生成します
- 生成ファイル
    - ツイート検索結果ファイル
        - ./dest/tweet_search_result/[クエリ].csv
- コマンド例
    - poetry run twitter search-tweet "API" -t 100

positional arguments:
  query                 - [グループA(必須)] クエリ
                            - RTと返信はデフォルトで除外します

options:
  -h, --help            show this help message and exit
  -t NUM_OF_TWEETS, --num_of_tweets NUM_OF_TWEETS
                        - [グループC(任意)] ツイート数 (デフォルト：100)
                            - 表示するツイートの数
                            - 18000件を超過した場合はレート制限により18000件ごとに15分の待機時間が発生します
```

#### 6.8.2. 実行結果

ツイート検索結果ファイルが生成される。

##### 6.8.2.1. ツイート検索結果ファイル

例として下記コマンドを実行する。

```shell
$ poetry run twitter search-tweet "API" -t 100
```

実行することにより、ファイルが下記パスに生成される。

| 種類         | ファイルパス                            |
| ------------ | --------------------------------------- |
| フォーマット | ./dest/tweet_search_result/[クエリ].csv |
| 例           | ./dest/tweet_search_result/API.csv      |

### 6.9. サブコマンド：Twitterツイート配信

#### 6.9.1. ヘルプ

下記コマンドでヘルプを呼び出す。

```shell
$ poetry run twitter stream-tweet -h
[INF][         MainProcess][          MainThread][                                 main.py:0021][                                    main] コマンド：['twitter', 'stream-tweet', '-h']
[INF][         MainProcess][          MainThread][                           arg_parser.py:0046][                          _print_message] 
usage: twitter stream-tweet [-h] [-ui USER_ID_FOR_FOLLOWEES | -li LIST_ID | -ln LIST_NAME | -fp FILE_PATH HEADER_LINE_NUM] [-k KEYWORD_OF_CSV_FORMAT]

- 機能名
    - Twitterツイート配信
- 概要
    - 指定したキーワードのツイートを配信します
- コマンド例
    - poetry run twitter stream-tweet -ui "silverag_corgi" -k "Google Docs, Google Drive"
    - poetry run twitter stream-tweet -li "0123456789111111111" -k "Google Docs, Google Drive"
    - poetry run twitter stream-tweet -ln "Google関連" -k "Google Docs, Google Drive"
    - poetry run twitter stream-tweet -fp "input/list_member/*.csv" 1 -k "Google Docs, Google Drive"

options:
  -h, --help            show this help message and exit
  -ui USER_ID_FOR_FOLLOWEES, --user_id_for_followees USER_ID_FOR_FOLLOWEES
                        - [グループB1(1つのみ必須)] ユーザID(フォロイー用)
                            - 指定したユーザIDのフォロイーのツイートを配信します
  -li LIST_ID, --list_id LIST_ID
                        - [グループB1(1つのみ必須)] リストID
                            - 指定したリストIDのツイートを配信します
  -ln LIST_NAME, --list_name LIST_NAME
                        - [グループB1(1つのみ必須)] リスト名
                            - 指定したリスト名のツイートを配信します
  -fp FILE_PATH HEADER_LINE_NUM, --following_user_file_path FILE_PATH HEADER_LINE_NUM
                        - [グループB1(1つのみ必須)] フォローユーザファイルパス(csvファイル) ヘッダ行番号
                            - 指定したファイルに記載されているユーザのツイートを配信します
                            - またヘッダ行番号は 0：ヘッダなし 1~：ヘッダとなるファイルの行番号 です
  -k KEYWORD_OF_CSV_FORMAT, --keyword_of_csv_format KEYWORD_OF_CSV_FORMAT
                        - [グループC(任意)] キーワード(csv形式)
                            - 例："Google Docs, Google Drive"
                            - スペースはAND検索(Google AND Docs)
                            - カンマはOR検索(Google Docs OR Google Drive)
```

#### 6.9.2. 実行結果

Twitterツイートが配信される。

##### 6.9.2.1. Twitterツイート

例として下記コマンドを実行する。

```shell
$ poetry run twitter stream-tweet -ui "silverag_corgi" -k "Google Docs, Google Drive"
$ poetry run twitter stream-tweet -li "0123456789111111111" -k "Google Docs, Google Drive"
$ poetry run twitter stream-tweet -ln "Google関連" -k "Google Docs, Google Drive"
$ poetry run twitter stream-tweet -fp "input/list_member/*.csv" 1 -k "Google Docs, Google Drive"
```

## 7. 連絡先

[Twitter(@silverag_corgi)](https://twitter.com/silverag_corgi)

## 8. ライセンス

MITライセンスの下で公開している。
詳細はLICENSEを確認すること。

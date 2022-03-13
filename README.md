# twitter-app <!-- omit in toc -->


# 0. 目次 <!-- omit in toc -->

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
  - [6.1. Twitterリストインポート](#61-twitterリストインポート)
    - [6.1.1. TwitterリストCSVファイルの作成](#611-twitterリストcsvファイルの作成)
    - [6.1.2. プログラムの実行](#612-プログラムの実行)
  - [6.2. Twitterリストエクスポート](#62-twitterリストエクスポート)
    - [6.2.1. プログラムの実行](#621-プログラムの実行)
  - [6.3. Twitterフォロイー(フォロワー)リスト生成](#63-twitterフォロイーフォロワーリスト生成)
    - [6.3.1. プログラムの実行](#631-プログラムの実行)
  - [6.4. Twitterツイート検索](#64-twitterツイート検索)
    - [6.4.1. プログラムの実行](#641-プログラムの実行)
  - [6.5. Twitterレート制限表示](#65-twitterレート制限表示)
    - [6.5.1. プログラムの実行](#651-プログラムの実行)
  - [6.6. TwitterPIN認証](#66-twitterpin認証)
    - [6.6.1. プログラムの実行](#661-プログラムの実行)
- [7. 連絡先](#7-連絡先)
- [8. ライセンス](#8-ライセンス)


# 1. 概要

TwitterAPIを利用したアプリケーション。


# 2. 機能

アプリケーションとしてコマンドラインから実行できる。

- Twitterリストインポート
  - 指定したCSVファイルをTwitterリストとしてTwitterにインポートする
- Twitterリストエクスポート
  - 指定したTwitterリストをTwitterからエクスポートする
- Twitterフォロイー(フォロワー)リスト生成
  - 指定したTwitterユーザのフォロイー(フォロワー)のTwitterリストを生成する
- Twitterツイート検索
  - 指定したクエリでツイートを検索し、ツイート検索結果ファイルを生成する
- Twitterレート制限表示
  - 指定したリソース群とエンドポイントのレート制限を表示する
- TwitterPIN認証
  - コンシューマーキーとPINコードを基にアクセストークンを生成し、認証情報ファイルに保存する


# 3. 動作確認済み環境

- Windows 10 Pro
- Python 3.10.1
- Poetry 1.1.12
- Tweepy 4.4.0


# 4. 事前準備


## 4.1. TwitterAPI認証情報の発行

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


### 4.1.1. (A)Twitter開発者ポータルサイトで申請する手順

[Twitter Developer Portal](https://developer.twitter.com/en/apply-for-access)
で認証情報を発行する。
発行手順は長くなる上に頻繁に仕様が変更されるため
[ググる](https://www.google.com/search?q=TwitterAPI+申請)
こと。

また、以下の通り設定する。

|   No | 設定項目                                       | 設定値                            | 備考   |
| ---: | ---------------------------------------------- | --------------------------------- | ------ |
|   01 | User authentication settings - Methods         | OAuth 1.0a                        |        |
|   02 | User authentication settings - App permissions | Read and write and Direct message |        |
|   03 | Consumer Keys - API Key                        | (自動生成値)                      | (1)    |
|   04 | Consumer Keys - API Secret                     | (自動生成値)                      | (1)    |
|   05 | Authentication Tokens - Access Token           | (自動生成値)                      | (2)(3) |
|   06 | Authentication Tokens - Access Token Secret    | (自動生成値)                      | (2)(3) |
|   07 | Access levels                                  | Elevated                          | (4)    |

(1)アプリの認証情報。アプリとは、Twitterクライアント(TweetDeckなど)やTwitter管理ツール(SocialDogなど)のこと。

(2)ユーザの認証情報。ユーザとは、Twitterアカウントのこと。

(3)`App permissions`を変更した場合は再生成する必要がある。

(4)`Twitter API v1.1`を使用するため、`Essential`からのアップグレードを申請する必要がある。


### 4.1.2. (B)Twitter社が公開しているコンシューマーキーとPINコードにより発行する手順

[Twitter Official/unOfficial Credentials - Twitter for Mac](https://gist.github.com/shobotch/5160017#twitter-for-mac)
に掲載されている下記項目を利用する。

- Consumer Key = API Key
- Consumer Secret = API Secret

ここで本項は一旦保留する。

[5.2. 仮想環境の構築](#52-仮想環境の構築)
まで完了した後に、上記項目を用いて
[5.3. TwitterAPI認証情報の設定](#53-twitterapi認証情報の設定)
及び
[6.5. TwitterPIN認証](#65-twitterpin認証)
を実行する。


# 5. セットアップ手順

前提として、PythonとPoetryがインストール済みであること。


## 5.1. リポジトリのクローン

下記リポジトリをクローンもしくはダウンロードする。

- twitter-app
  - 本リポジトリ
- python-lib-for-me
  - 自分用のPythonライブラリ


## 5.2. 仮想環境の構築

下記コマンドを実行する。

```cmd
> cd twitter-app                            # アプリケーションのパスに移動する
> poetry config virtualenvs.in-project true # 仮想環境のインストール先をプロジェクト配下に設定する
> poetry install                            # pyproject.tomlを基に仮想環境をインストールする
```

そして、下記コマンドを実行して、アプリケーション配下に`.venv`フォルダが作成されていることを確認する。

```cmd
> poetry env info --path                    # 仮想環境のインストール先を表示する
C:\Git\python\twitter-app\.venv
```


## 5.3. TwitterAPI認証情報の設定

`config/twitter_api_auth_info.json.sample`をコピペし、拡張子`.sample`を削除し、発行した認証情報を保存する。

認証情報の保存例：
```cmd
> type config\twitter_api_auth_info.json 
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


# 6. 使い方

アプリケーションの実行手順を機能ごとに示す。


## 6.1. Twitterリストインポート


### 6.1.1. TwitterリストCSVファイルの作成

`input/twitter_list_name.csv.sample`をコピペし、拡張子`.sample`を削除し、作成したいリスト名にリネームする。

CSVファイルの配置例：
```cmd
> cd twitter-app/input
> dir
yyyy/mm/dd  hh:nn    <DIR>          .
yyyy/mm/dd  hh:nn    <DIR>          ..
yyyy/mm/dd  hh:nn                74 Google.csv
yyyy/mm/dd  hh:nn                25 twitter_list_name.csv.sample
```

次にCSV形式でリストに追加したいユーザ(ユーザID、ユーザ名)を保存する。

CSVファイルの保存例：
```cmd
> type Google.csv
googledocs,Google Docs
googledrive,Google Drive
googlemaps,Google Maps
```


### 6.1.2. プログラムの実行

下記コマンドを実行する。

実行例：
```cmd
> cd twitter-app
> poetry run list-import -t input/*.csv
```

また、ヘルプを呼び出す時は下記コマンドを実行する。

```cmd
> poetry run list-import -h 
usage: list-import [-h] [-t TWITTER_LIST_CSV_FILE_PATH] [-hd HEADER_LINE_NUM]

options:
  -h, --help            show this help message and exit
  -t TWITTER_LIST_CSV_FILE_PATH, --twitter_list_csv_file_path TWITTER_LIST_CSV_FILE_PATH
                        TwitterリストCSVファイルパス(csv) (default: input/*.csv)
                        ワイルドカード可
  -hd HEADER_LINE_NUM, --header_line_num HEADER_LINE_NUM
                        ヘッダ行番号 (default: 1)
                        0：ヘッダなし、1~：ヘッダとなるファイルの行番号
```


## 6.2. Twitterリストエクスポート


### 6.2.1. プログラムの実行

下記コマンドを実行する。

実行例：
```cmd
> cd twitter-app
> poetry run list-exp -s -name "Google関連アカウント, Microsoft関連アカウント"
```

また、ヘルプを呼び出す時は下記コマンドを実行する。

```cmd
> poetry run list-exp -h
usage: list-exp [-h] (-s | -e) (-all | -id TWITTER_LIST_ID | -name TWITTER_LIST_NAME)

Twitterリストエクスポート
指定したTwitterリストをTwitterからエクスポートする

options:
  -h, --help            show this help message and exit

グループA:
  実行する処理を選択する

  -s, --show_twitter_list
                        [1つのみ必須] Twitterリスト表示要否
                        指定した場合はTwitterリストを表示する
  -e, --export_twitter_list
                        [1つのみ必須] Twitterリストエクスポート要否
                        指定した場合はTwitterリストをエクスポートする

グループB:
  処理対象のTwitterリストを選択する

  -all, --all_twitter_list
                        [1つのみ必須] 全てのTwitterリスト
  -id TWITTER_LIST_ID, --twitter_list_id TWITTER_LIST_ID
                        [1つのみ必須] TwitterリストID (csv形式)
                        例："0123456789111111111, 0123456789222222222"
  -name TWITTER_LIST_NAME, --twitter_list_name TWITTER_LIST_NAME
                        [1つのみ必須] Twitterリスト名 (csv形式)
                        例："Google関連アカウント, Microsoft関連アカウント"
```


## 6.3. Twitterフォロイー(フォロワー)リスト生成


### 6.3.1. プログラムの実行

下記コマンドを実行する。

実行例：
```cmd
> cd twitter-app
> poetry run followxx-gen Google -followee
```

また、ヘルプを呼び出す時は下記コマンドを実行する。

```cmd
> poetry run followxx-gen -h
usage: followxx-gen [-h] (-followee | -follower) [-f NUM_OF_FOLLOWXXS] user_id

positional arguments:
  user_id               ユーザID(Twitter)

options:
  -h, --help            show this help message and exit
  -followee, --generate_followee_list
                        フォロイーリスト生成
                        グループで1つのみ必須
                        指定した場合はフォロイーのTwitterリストを生成する
  -follower, --generate_follower_list
                        フォロワーリスト生成
                        グループで1つのみ必須
                        指定した場合はフォロワーのTwitterリストを生成する
  -f NUM_OF_FOLLOWXXS, --num_of_followxxs NUM_OF_FOLLOWXXS
                        フォロイー(フォロワー)数 (default: 3000)
                        Twitterリストに追加したいフォロイー(フォロワー)の人数
                        3000人を超過した場合はレート制限により3000人ごとに15分の待機時間が発生する
```


## 6.4. Twitterツイート検索


### 6.4.1. プログラムの実行

下記コマンドを実行する。

実行例：
```cmd
> cd twitter-app
> poetry run tweet-search #FGO
```

また、ヘルプを呼び出す時は下記コマンドを実行する。

```cmd
> poetry run tweet-search -h
usage: tweet-search [-h] [-t NUM_OF_TWEETS] query

positional arguments:
  query                 クエリ
                        RTと返信はデフォルトで除外する

options:
  -h, --help            show this help message and exit
  -t NUM_OF_TWEETS, --num_of_tweets NUM_OF_TWEETS
                        ツイート数 (default: 100)
                        表示したいツイートの数
                        18000件を超過した場合はレート制限により18000件ごとに15分の待機時間が発生する
```


## 6.5. Twitterレート制限表示


### 6.5.1. プログラムの実行

下記コマンドを実行する。

実行例：
```cmd
> cd twitter-app
> poetry run limit-show "friends" "/friends/list"
```

また、ヘルプを呼び出す時は下記コマンドを実行する。

```cmd
> poetry run limit-show -h
usage: limit-show [-h] resource_family endpoint

positional arguments:
  resource_family  リソース群
                   例：application
  endpoint         エンドポイント
                   例：/application/rate_limit_status
                   両方とも空文字の場合は全てのレート制限を表示します

options:
  -h, --help       show this help message and exit
```


## 6.6. TwitterPIN認証


### 6.6.1. プログラムの実行

下記コマンドを実行する。

実行例：
```cmd
> cd twitter-app
> poetry run pin-auth
```

また、ヘルプを呼び出す時は下記コマンドを実行する。

```cmd
> poetry run pin-auth -h
usage: pin-auth [-h]

options:
  -h, --help  show this help message and exit
```


# 7. 連絡先

[Twitter(@silverag_corgi)](https://twitter.com/silverag_corgi)


# 8. ライセンス

MITライセンスの下で公開している。
詳細はLICENSEを確認すること。


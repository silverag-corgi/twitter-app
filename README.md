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
    - [6.1.1. リストメンバーファイルの作成](#611-リストメンバーファイルの作成)
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
  - [6.7. Twitterツイート配信](#67-twitterツイート配信)
    - [6.7.1. プログラムの実行](#671-プログラムの実行)
- [7. 実行コマンド一覧](#7-実行コマンド一覧)
- [8. 連絡先](#8-連絡先)
- [9. ライセンス](#9-ライセンス)


# 1. 概要

TwitterAPIを利用したアプリケーション。


# 2. 機能

アプリケーションとしてコマンドラインから実行できる。

- Twitterリストインポート
  - 指定したCSVファイルをリストとしてTwitterにインポートする
- Twitterリストエクスポート
  - 指定したリストをTwitterからエクスポートする
- Twitterフォロイー(フォロワー)リスト生成
  - 指定したユーザのフォロイー(フォロワー)のリストを生成する
- Twitterツイート検索
  - 指定したクエリでツイートを検索し、ツイート検索結果ファイルを生成する
- Twitterレート制限表示
  - 指定したリソース群とエンドポイントのレート制限を表示する
- TwitterPIN認証
  - コンシューマーキーとPINコードを基にアクセストークンを生成し、認証情報ファイルに保存する
- Twitterツイート配信
  - 指定したキーワードのツイートを配信する


# 3. 動作確認済み環境

- Windows 10 Pro
- [Python 3.10.1](https://www.python.org/downloads/release/python-3101/)
- [Poetry 1.1.12](https://python-poetry.org/docs/#installing-with-pip)


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
[ググる](https://www.google.com/search?q=TwitterAPI+申請+解説)
こと。
2022年3月時点では
[Twitter APIの申請方法を解説【2022年版】](https://mitchieblog.com/twitter-api-apply/)
を参考に申請するとよい。

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
[6.6. TwitterPIN認証](#66-twitterpin認証)
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


### 6.1.1. リストメンバーファイルの作成

1. リストメンバーサンプルファイル`input/list_member.csv.sample`をコピペする
2. 拡張子`.sample`を削除する
3. 作成したいリスト名にリネームする
4. CSV形式でリストに追加したいユーザ(ユーザID、ユーザ名)を記入する

リストメンバーサンプルファイル：
```cmd
> type list_member.csv.sample
user_id,user_name
googledocs,Google Docs
googledrive,Google Drive
googlemaps,Google Maps
```

また、後述の
[6.2. Twitterリストエクスポート](#62-twitterリストエクスポート)
の出力ファイルがリストメンバーファイルであるため、入力ファイルになる。


### 6.1.2. プログラムの実行

下記コマンドを実行する。

実行例：
```cmd
> cd twitter-app
> poetry run list-imp -l input/*.csv
```

また、ヘルプを呼び出す時は下記コマンドを実行する。

```cmd
> poetry run list-imp -h 
usage: list-imp [-h] [-l LIST_MEMBER_FILE_PATH] [-hd HEADER_LINE_NUM]

Twitterリストインポート
指定したCSVファイルをリストとしてTwitterにインポートします

options:
  -h, --help            show this help message and exit
  -l LIST_MEMBER_FILE_PATH, --list_member_file_path LIST_MEMBER_FILE_PATH
                        [任意] リストメンバーファイルパス (デフォルト：input/*.csv)
                        ワイルドカード可
  -hd HEADER_LINE_NUM, --header_line_num HEADER_LINE_NUM
                        [任意] ヘッダ行番号 (デフォルト：1)
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
usage: list-exp [-h] (-s | -e) (-all | -id LIST_ID | -name LIST_NAME)

Twitterリストエクスポート
指定したリストをTwitterからエクスポートします

options:
  -h, --help            show this help message and exit

options in this group:
  実行する処理を指定します

  -s, --show_list       [1つのみ必須] リスト表示要否
                        指定した場合はリストを表示します
  -e, --export_list     [1つのみ必須] リストエクスポート要否
                        指定した場合はリストをエクスポートします

options in this group:
  処理対象のリストを指定します

  -all, --all_list      [1つのみ必須] 全てのリスト
  -id LIST_ID, --list_id LIST_ID
                        [1つのみ必須] リストID(csv形式)
                        例："0123456789111111111, 0123456789222222222"
  -name LIST_NAME, --list_name LIST_NAME
                        [1つのみ必須] リスト名(csv形式)
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

Twitterフォロイー(フォロワー)リスト生成
指定したユーザのフォロイー(フォロワー)のリストを生成します

positional arguments:
  user_id               [必須] ユーザID

options:
  -h, --help            show this help message and exit
  -f NUM_OF_FOLLOWXXS, --num_of_followxxs NUM_OF_FOLLOWXXS
                        [任意] フォロイー(フォロワー)数 (デフォルト：3000)
                        リストに追加したいフォロイー(フォロワー)の人数
                        3000人を超過した場合はレート制限により3000人ごとに15分の待機時間が発生します

options in this group:
  実行する処理を指定します

  -followee, --generate_followee_list
                        [1つのみ必須] フォロイーリスト生成
                        指定した場合はフォロイーのリストを生成します
  -follower, --generate_follower_list
                        [1つのみ必須] フォロワーリスト生成
                        指定した場合はフォロワーのリストを生成します
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

Twitterツイート検索
指定したクエリでツイートを検索し、ツイート検索結果ファイルを生成します

positional arguments:
  query                 [必須] クエリ
                        RTと返信はデフォルトで除外します

options:
  -h, --help            show this help message and exit
  -t NUM_OF_TWEETS, --num_of_tweets NUM_OF_TWEETS
                        [任意] ツイート数 (デフォルト：100)
                        表示したいツイートの数
                        18000件を超過した場合はレート制限により18000件ごとに15分の待機時間が発生します
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

Twitterレート制限表示
指定したリソース群とエンドポイントのレート制限を表示します

options:
  -h, --help       show this help message and exit

positional arguments in this group:
  表示するレート制限を指定します
  両方とも空文字の場合は全てのレート制限を表示します

  resource_family  [必須] リソース群
                   例：application
  endpoint         [必須] エンドポイント
                   例：/application/rate_limit_status
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

TwitterPIN認証
コンシューマーキーとPINコードを基にアクセストークンを生成し、認証情報ファイルに保存します

options:
  -h, --help  show this help message and exit
```


## 6.7. Twitterツイート配信


### 6.7.1. プログラムの実行

下記コマンドを実行する。

実行例：
```cmd
> cd twitter-app
> poetry run tweet-stream -u silverag_corgi
```

また、ヘルプを呼び出す時は下記コマンドを実行する。

```cmd
> poetry run tweet-stream -h
usage: tweet-stream [-h] (-u USER_ID_FOR_FOLLOWEES | -l LIST_ID) [-k KEYWORD_OF_CSV_FORMAT]

Twitterツイート配信
指定したキーワードのツイートを配信します

options:
  -h, --help            show this help message and exit
  -k KEYWORD_OF_CSV_FORMAT, --keyword_of_csv_format KEYWORD_OF_CSV_FORMAT
                        [任意] キーワード(csv形式)
                        例："Google Docs, Google Drive"
                        スペースはAND検索(Google AND Docs)
                        カンマはOR検索(Google Docs OR Google Drive)

options in this group:
  処理対象のIDを指定します

  -u USER_ID_FOR_FOLLOWEES, --user_id_for_followees USER_ID_FOR_FOLLOWEES
                        [1つのみ必須] ユーザID(フォロイー用)
                        指定したユーザIDのフォロイーのツイートを配信する
  -l LIST_ID, --list_id LIST_ID
                        [1つのみ必須] リストID
                        指定したリストIDのツイートを配信する
```


# 7. 実行コマンド一覧

```cmd
> poetry run list-imp     -h
> poetry run list-exp     -h
> poetry run followxx-gen -h
> poetry run tweet-search -h
> poetry run limit-show   -h
> poetry run pin-auth     -h
> poetry run tweet-stream -h
```


# 8. 連絡先

[Twitter(@silverag_corgi)](https://twitter.com/silverag_corgi)


# 9. ライセンス

MITライセンスの下で公開している。
詳細はLICENSEを確認すること。


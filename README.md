# twitter-lib-for-me <!-- omit in toc -->


# 0. 目次 <!-- omit in toc -->

- [1. 概要](#1-概要)
- [2. 機能](#2-機能)
- [3. 動作確認済み環境](#3-動作確認済み環境)
- [4. 事前準備 - Twitter認証情報の発行](#4-事前準備---twitter認証情報の発行)
- [5. セットアップ手順 - アプリケーション](#5-セットアップ手順---アプリケーション)
  - [5.1. リポジトリのクローン](#51-リポジトリのクローン)
  - [5.2. 仮想環境の構築](#52-仮想環境の構築)
  - [5.3. Twitter認証情報の設定](#53-twitter認証情報の設定)
- [6. セットアップ手順 - ライブラリ](#6-セットアップ手順---ライブラリ)
  - [6.1. リポジトリのクローン](#61-リポジトリのクローン)
  - [6.2. 依存関係の追加](#62-依存関係の追加)
- [7. 使い方 - アプリケーション](#7-使い方---アプリケーション)
  - [7.1. Twitterリスト生成](#71-twitterリスト生成)
    - [7.1.1. ユーザ一覧CSVファイルの作成](#711-ユーザ一覧csvファイルの作成)
    - [7.1.2. プログラムの実行](#712-プログラムの実行)
  - [7.2. フォロイー／フォロワーTwitterリスト生成](#72-フォロイーフォロワーtwitterリスト生成)
    - [7.2.1. プログラムの実行](#721-プログラムの実行)
  - [7.3. Twitterツイート検索](#73-twitterツイート検索)
    - [7.3.1. プログラムの実行](#731-プログラムの実行)
- [8. 使い方 - ライブラリ](#8-使い方---ライブラリ)
- [9. 連絡先](#9-連絡先)
- [10. ライセンス](#10-ライセンス)


# 1. 概要

自分用のTwitterライブラリ。

PyPIには登録せずにローカルで使用する。


# 2. 機能

アプリケーションとライブラリの機能がある。

- Twitterリスト生成
  - ユーザ一覧のCSVファイルを基にTwitterリストを生成する
- フォロイー／フォロワーTwitterリスト生成
  - 指定したTwitterユーザのフォロイー／フォロワーのTwitterリストを生成する
- Twitterツイート検索
  - 指定したクエリでツイートを検索し、ツイート検索結果ファイルを生成する
- (今後、追加予定)


# 3. 動作確認済み環境

- Windows 10 Pro
- Python 3.10.1
- Poetry 1.1.12
- Tweepy 4.4.0


# 4. 事前準備 - Twitter認証情報の発行

[Twitter Developer Portal](https://developer.twitter.com/en/apply-for-access)
で認証情報を発行する。
発行手順は長くなる上に頻繁に仕様が変更されるため
[ググる](https://www.google.com/search?q=TwitterAPI+申請)
こと。

`TwitterAPI Standard v1.1`を使用するため、アクセスレベルを`Elevated`で発行する。

参考までに`Essential`、`Elevated`、`AcademicResearch`の順で高くなる。
各アクセスレベルで何ができるかは
[V2 Access Levels | Twitter API Documentation | Twitter Developer Platform](https://developer.twitter.com/en/docs/twitter-api)
を確認すること。


# 5. セットアップ手順 - アプリケーション

アプリケーションとライブラリの手順がある。
本章は前者の手順を示す。

また、前提として、PythonとPoetryがインストール済みであること。


## 5.1. リポジトリのクローン

下記リポジトリをクローンもしくはダウンロードする。

- twitter-lib-for-me
  - 本リポジトリ
- python-lib-for-me
  - 自分用のPythonライブラリ


## 5.2. 仮想環境の構築

下記コマンドを実行する。

```cmd
> cd twitter-lib-for-me                     # アプリケーションのパスに移動する
> poetry config virtualenvs.in-project true # 仮想環境のインストール先をプロジェクト配下に設定する
> poetry install                            # pyproject.tomlを基に仮想環境をインストールする
```

そして、下記コマンドを実行して、アプリケーション配下に`.venv`フォルダが作成されていることを確認する。

```cmd
> poetry env info --path                    # 仮想環境のインストール先を表示する
C:\Git\python\twitter-lib-for-me\.venv
```


## 5.3. Twitter認証情報の設定

`config/twitter_api_auth_info.json.sample`をコピペし、拡張子`.sample`を削除し、発行した認証情報を保存する。

認証情報の保存例：
```cmd
> type config\twitter_api_auth_info.json.sample
{
  "consumer_key"        : "xxxxx",
  "consumer_secret"     : "xxxxx",
  "access_token"        : "xxxxx",
  "access_token_secret" : "xxxxx"
}
```


# 6. セットアップ手順 - ライブラリ

アプリケーションとライブラリの手順がある。
本章は後者の手順を示す。

また、前提として、PythonとPoetryがインストール済みであること。


## 6.1. リポジトリのクローン

下記リポジトリをクローンもしくはダウンロードする。

- twitter-lib-for-me
  - 本リポジトリ
- python-lib-for-me
  - 自分用のPythonライブラリ


## 6.2. 依存関係の追加

下記コマンドを実行する。

```cmd
> cd [app_path]                             # ライブラリをインストールしたいアプリケーションのパスに移動する
> poetry add "../twitter-lib-for-me"        # 仮想環境にライブラリを追加する
```

もし、ライブラリを編集可能モードで追加する場合は、`pyproject.toml`ファイルに`develop = true`を追記する。

```toml
[tool.poetry.dependencies]
twitter-lib-for-me = {path = "../twitter-lib-for-me", develop = true}
```

下記コマンドを実行する。

```cmd
> poetry update                             # pyproject.tomlを基に仮想環境をアップデートする
```


# 7. 使い方 - アプリケーション

アプリケーションとライブラリの手順がある。
本章は前者の手順を機能ごとに示す。


## 7.1. Twitterリスト生成


### 7.1.1. ユーザ一覧CSVファイルの作成

`input/twitter_list_name.csv.sample`をコピペし、拡張子`.sample`を削除し、作成したいリスト名にリネームする。

CSVファイルの配置例：
```cmd
> cd twitter-lib-for-me/input
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


### 7.1.2. プログラムの実行

下記コマンドを実行する。

実行例：
```cmd
> cd twitter-lib-for-me
> poetry run list-gen -t input/*.csv
```

また、ヘルプを呼び出す時は下記コマンドを実行する。

```cmd
> poetry run list-gen -h
usage: twitter_list_gen.py [-h] [-t TWITTER_LIST_FILE_PATH]

options:
  -h, --help            show this help message and exit
  -t TWITTER_LIST_FILE_PATH, --twitter_list_file_path TWITTER_LIST_FILE_PATH
                        Twitterリストファイルパス (ワイルドカード可) (default: input/*.csv)
```


## 7.2. フォロイー／フォロワーTwitterリスト生成


### 7.2.1. プログラムの実行

下記コマンドを実行する。

実行例：
```cmd
> cd twitter-lib-for-me
> poetry run followxx-gen Google -followee
```

また、ヘルプを呼び出す時は下記コマンドを実行する。

```cmd
> poetry run followxx-gen -h
usage: followxx_twitter_list_gen.py [-h] (-followee | -follower) [-f NUM_OF_FOLLOWXXS] user_id

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
                        フォロイー数／フォロワー数 (default: 3000)
                        Twitterリストに追加したいフォロイー／フォロワーの人数
                        3000人を超過した場合はレート制限により3000人ごとに15分の待機時間が発生する
```


## 7.3. Twitterツイート検索


### 7.3.1. プログラムの実行

下記コマンドを実行する。

実行例：
```cmd
> cd twitter-lib-for-me
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


# 8. 使い方 - ライブラリ

アプリケーションとライブラリの手順がある。
本章は後者の手順を示す。

下記コードでアプリケーションから機能を呼び出す。

実装例：
```python
import twitter_lib_for_me
twitter_lib_for_me.do_function()
```


# 9. 連絡先

[Twitter(@silverag_corgi)](https://twitter.com/silverag_corgi)


# 10. ライセンス

MITライセンスの下で公開している。
詳細はLICENSEを確認すること。


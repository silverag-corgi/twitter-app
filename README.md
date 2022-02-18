# twitter-lib-for-me <!-- omit in toc -->


# 0. 目次 <!-- omit in toc -->

- [1. 概要](#1-概要)
- [2. 機能](#2-機能)
- [3. 動作確認済み環境](#3-動作確認済み環境)
- [4. 事前準備 - Twitter認証情報の発行](#4-事前準備---twitter認証情報の発行)
- [5. セットアップ手順 - アプリケーション](#5-セットアップ手順---アプリケーション)
  - [5.1. 仮想環境の構築](#51-仮想環境の構築)
  - [5.2. Twitter認証情報の設定](#52-twitter認証情報の設定)
- [6. セットアップ手順 - ライブラリ](#6-セットアップ手順---ライブラリ)
- [7. 使い方 - アプリケーション](#7-使い方---アプリケーション)
  - [7.1. Twitterリスト生成](#71-twitterリスト生成)
    - [7.1.1. ユーザ一覧CSVファイルの作成](#711-ユーザ一覧csvファイルの作成)
    - [7.1.2. プログラムの実行](#712-プログラムの実行)
  - [7.2. フォロイーTwitterリスト生成](#72-フォロイーtwitterリスト生成)
    - [7.2.1. プログラムの実行](#721-プログラムの実行)
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
- フォロイーTwitterリスト生成
  - 指定したTwitterユーザのフォロイーのTwitterリストを生成する
- (今後、追加予定)


# 3. 動作確認済み環境

- Windows 10 Pro
- Python 3.10.1
- Pipenv 2022.1.8
- Tweepy 4.4.0


# 4. 事前準備 - Twitter認証情報の発行

[Twitter Developers](https://developer.twitter.com/en/portal/dashboard)
で認証情報を発行する。
発行手順は長くなる上に頻繁に仕様が変更されるため
[ググる](https://www.google.com/search?q=TwitterAPI+利用申請)
こと。

アクセスレベルはElevatedで発行する。
参考までにEssential＜Elevated＜AcademicResearch。


# 5. セットアップ手順 - アプリケーション

アプリケーションとライブラリの手順がある。
本章は前者の手順を示す。

また、前提として、PythonとPipenvがインストール済みであること。


## 5.1. 仮想環境の構築

本リポジトリをクローンもしくはダウンロードした後、下記コマンドを実行する。

実行例：
```cmd
> cd twitter-lib-for-me           # アプリケーションのパスに移動する
> set PIPENV_VENV_IN_PROJECT=true # 仮想環境のインストール先をアプリケーション配下に設定する
> pipenv install                  # 仮想環境をインストールする
```

そして、下記コマンドを実行して、アプリケーション配下に`.venv`フォルダが作成されていることを確認する。

実行例：
```cmd
> pipenv --venv                   # 仮想環境のインストール先を表示する
C:/Git/python/twitter-lib-for-me/.venv
```


## 5.2. Twitter認証情報の設定

`config/api_auth_info.json.sample`をコピペし、拡張子`.sample`を削除し、発行した認証情報を保存する。

認証情報の保存例：
```cmd
> type config\api_auth_info.json
{
  "twitter_auth": {
    "consumer_key"        : "xxxxxxxxxxxxxxxxxxxxxxxxx",
    "consumer_secret"     : "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "access_token"        : "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "access_token_secret" : "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }
}
```


# 6. セットアップ手順 - ライブラリ

アプリケーションとライブラリの手順がある。
本章は後者の手順を示す。

また、前提として、PythonとPipenvがインストール済みであること。

本リポジトリをクローンもしくはダウンロードした後、下記コマンドを実行する。

実行例：
```cmd
> cd fgo-farm-report-collection             # ライブラリをインストールしたいアプリケーションのパスに移動する
> pipenv install -e "../twitter-lib-for-me" # ライブラリのパスを指定して編集モードでインストールする
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
> pipenv run list-gen -t 'input/*.csv'
```

また、ヘルプを呼び出す時は下記コマンドを実行する。

実行例：
```cmd
> pipenv run list-gen -h
usage: twitter_list_gen.py [-h] [-t TWITTER_LIST_FILE_PATH]

options:
  -h, --help            show this help message and exit
  -t TWITTER_LIST_FILE_PATH, --twitter_list_file_path TWITTER_LIST_FILE_PATH
                        Twitterリストファイルパス (ワイルドカード可) (default: input/*.csv)
                        必ずシングルコーテーション(')で囲む。
```


## 7.2. フォロイーTwitterリスト生成


### 7.2.1. プログラムの実行

下記コマンドを実行する。

実行例：
```cmd
> cd twitter-lib-for-me
> pipenv run followee-gen Google
```

また、ヘルプを呼び出す時は下記コマンドを実行する。

実行例：
```cmd
> pipenv run followee-gen -h
usage: followee_twitter_list_gen.py [-h] [-f NUM_OF_FOLLOWEES] user_id

positional arguments:
  user_id               ユーザID(Twitter)

options:
  -h, --help            show this help message and exit
  -f NUM_OF_FOLLOWEES, --num_of_followees NUM_OF_FOLLOWEES
                        フォロイー数 (default: 3000)
                        Twitterリストに追加したいフォロイーの人数
                        3000人を超過した場合はレート制限により3000人ごとに15分の待機時間が発生する
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


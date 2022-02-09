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
  - [7.1. Twitterリスト作成](#71-twitterリスト作成)
    - [7.1.1. ユーザ一覧CSVファイルの作成](#711-ユーザ一覧csvファイルの作成)
    - [7.1.2. プログラムの実行](#712-プログラムの実行)
- [8. 使い方 - ライブラリ](#8-使い方---ライブラリ)
- [9. 連絡先](#9-連絡先)
- [10. ライセンス](#10-ライセンス)


# 1. 概要

自分用のPythonライブラリ。

PyPIには登録せずにローカルで使用する。


# 2. 機能

アプリケーションとライブラリの機能がある。

- Twitterリスト作成
  - ユーザ一覧のCSVファイルを基にTwitterでリストを作成する
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

Installing -e ../twitter-lib-for-me...
Adding twitter-lib-for-me to Pipfile's [packages]...
Installation Succeeded
Pipfile.lock (e4eef2) out of date, updating to (d53d74)...
Locking [dev-packages] dependencies...
Locking [packages] dependencies...
 Locking...Building requirements...
Resolving dependencies...
Success!
Updated Pipfile.lock (d53d74)!
Installing dependencies from Pipfile.lock (d53d74)...
  ================================ 0/0 - 00:00:00
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```


# 7. 使い方 - アプリケーション

アプリケーションとライブラリの手順がある。
本章は前者の手順を機能ごとに示す。


## 7.1. Twitterリスト作成


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
> pipenv run list-gen -csv "input/*.csv"
[2022-02-09 08:46:25.430][INF][api_auth:0033][__get_api_auth_info_json] API認証情報JSON取得に成功しました。
[2022-02-09 08:46:25.655][INF][api_auth:0061][__exec_twitter_auth] Twitter認証実行に成功しました。
[2022-02-09 08:46:26.060][INF][twitter_list_util:0038][generate_twitter_list] Twitterリスト作成に成功しました。(リスト名：Google)
[2022-02-09 08:46:26.345][INF][twitter_list_util:0056][add_user] ユーザ追加に成功しました。(ユーザID：googledocs          、ユーザ名：Google Docs)
[2022-02-09 08:46:26.587][INF][twitter_list_util:0056][add_user] ユーザ追加に成功しました。(ユーザID：googledrive         、ユーザ名：Google Drive)
[2022-02-09 08:46:26.972][INF][twitter_list_util:0056][add_user] ユーザ追加に成功しました。(ユーザID：googlemaps          、ユーザ名：Google Maps)
```

また、ヘルプを呼び出す時は下記コマンドを実行する。

実行例：
```cmd
> pipenv run list-gen -h
usage: twitter_list_gen.py [-h] [-csv CSV_FILE_PATH]

options:
  -h, --help            show this help message and exit
  -csv CSV_FILE_PATH, --csv_file_path CSV_FILE_PATH
                        csv file path (regex enabled) (default: input/*.csv)
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


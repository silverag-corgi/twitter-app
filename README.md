# twitter-lib-for-me


# 1.概要

自分用のTwitterライブラリ。PyPIには登録しない。


# 2.機能

リポジトリ単体で起動する機能と、ライブラリとして使用する機能がある。

- Twitterリスト作成
  - ユーザ一覧のCSVファイルを基にTwitterでリストを作成する
- (今後、追加予定)


# 3.動作確認済み環境

- Windows 10 Pro
- Python 3.10.1
- Pipenv 2022.1.8
- Tweepy 4.4.0


# 4.事前準備 - Twitter認証情報の発行

[Twitter Developers](https://developer.twitter.com/en/portal/dashboard)
で認証情報を発行する。
発行手順は長くなる上に頻繁に仕様が変更されるため
[ググる](https://www.google.com/search?q=TwitterAPI+利用申請)
こと。

アクセスレベルはElevatedで発行する。
参考までにEssential＜Elevated＜AcademicResearch。


# 5.セットアップ手順 - リポジトリ単体で起動する場合

リポジトリ単体で起動する場合と、ライブラリとして使用する場合の手順がある。
本章は前者の手順を示す。

また、PythonとPipenvはインストール済みであることを前提とする。


## 5.1.仮想環境の構築

本プロジェクトをクローンもしくはダウンロードした後、以下のコマンドを実行する。

実行例：
```cmd
> cd twitter-lib-for-me
> set PIPENV_VENV_IN_PROJECT=true
> pipenv install
```

そして、以下のコマンドを実行して、本プロジェクトのフォルダ配下に`.venv`フォルダが作成されていることを確認する。

実行例：
```cmd
> pipenv --venv
C:/Git/python/twitter-lib-for-me/.venv
```


## 5.2.Twitter認証情報の設定

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


# 6.セットアップ手順 - ライブラリとして使用する場合

準備中。。。


# 7.使い方 - リポジトリ単体で起動する場合

リポジトリ単体で起動する場合と、ライブラリとして使用する場合の手順がある。
本章は前者の手順を機能ごとに示す。


## 7.1.Twitterリスト作成


### 7.1.1.ユーザ一覧CSVファイルの作成

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


### 7.1.2.プログラムの実行

以下のコマンドを実行する。

実行例：
```cmd
> cd twitter-lib-for-me
> pipenv run py -m src.main.twitter_list_gen -csv "input/*.csv"
API認証情報JSON取得に成功しました。
Twitter認証実行に成功しました。
Twitterリスト作成に成功しました。(リスト名：Google)
ユーザ追加に成功しました。(ユーザID：googledocs          、ユーザ名：Google Docs)
ユーザ追加に成功しました。(ユーザID：googledrive         、ユーザ名：Google Drive)
ユーザ追加に成功しました。(ユーザID：googlemaps          、ユーザ名：Google Maps)
```

また、ヘルプを呼び出す時は以下のコマンドを実行する。

実行例：
```cmd
> pipenv run py -m src.main.twitter_list_gen -h
usage: twitter_list_gen.py [-h] [-csv CSV_FILE_PATH]

options:
  -h, --help            show this help message and exit
  -csv CSV_FILE_PATH, --csv_file_path CSV_FILE_PATH
                        csv file path (regex enabled) (default: input/*.csv)
```


# 8.使い方 - ライブラリとして使用する場合

準備中。。。


# 9.連絡先

[Twitter(@silverag_corgi)](https://twitter.com/silverag_corgi)


# 10.ライセンス

MITライセンスの下で公開している。
詳細はLICENSEを確認すること。


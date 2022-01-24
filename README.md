# twitter-list-generator


# 概要


ユーザ一覧のcsvファイルを基にTwitterでリストを作成する。


# 動作確認済み環境

- Windows 10 Pro
- Python 3.10.1
- Tweepy 4.4.0


# セットアップ手順

本プロジェクトをクローンもしくはダウンロードした後、以下のコマンドを実行する。

```cmd
> cd twitter-list-generator
> pip install -r requirements.txt
```

次に
[Twitter Developers](https://developer.twitter.com/en/portal/dashboard)
で認証情報を発行する。
発行手順は長くなる上に頻繁に仕様が変更されるため
[ググる](https://www.google.com/search?q=TwitterAPI+利用申請)
こと。
また、アクセスレベルは ①Essential、②Elevated、③AcademicResearch の内、②以上にする必要がある。

そして、`config/api_auth_info.json.sample`をコピペし、拡張子`.sample`を削除し、発行した認証情報を保存する。


# 使い方


## ユーザ一覧CSVファイルの作成

`input/twitter_list_name.csv.sample`をコピペし、拡張子`.sample`を削除し、作成したいリスト名にリネームする。

CSVファイルの配置例：
```cmd
> cd twitter-list-generator/input
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


## プログラムの実行

以下のコマンドを実行する。

実行例：
```cmd
> cd twitter-list-generator
> py -m src -csv "input/*.csv"
API認証情報JSON取得に成功しました。
Twitter認証実行に成功しました。
Twitterリスト作成に成功しました。(リスト名：Google)
ユーザ追加に成功しました。(ユーザID：googledocs          、ユーザ名：Google Docs)
ユーザ追加に成功しました。(ユーザID：googledrive         、ユーザ名：Google Drive)
ユーザ追加に成功しました。(ユーザID：googlemaps          、ユーザ名：Google Maps)
```

また、ヘルプを呼び出す時は以下のコマンドを実行する。

```cmd
> py -m src -h
usage: __main__.py [-h] [-csv CSV_FILE_PATH]

options:
  -h, --help            show this help message and exit
  -csv CSV_FILE_PATH, --csv_file_path CSV_FILE_PATH
                        csv file path (regex enabled) (default: input/*.csv)
```


# 連絡先

[Twitter(@silverag_corgi)](https://twitter.com/silverag_corgi)


# ライセンス

MITライセンスの下で公開している。
詳細はLICENSEを確認すること。


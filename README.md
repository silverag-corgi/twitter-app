# twitter-list-generator


# 概要


ユーザ一覧のcsvファイルを基にTwitterでリストを作成する。

その際にcsvファイル名がリストの名前になる。
また、既にリストが作成されていた場合は作成をスキップする。


# 動作確認済み環境

- Windows 10 Pro
- Python 3.10.1
- Tweepy 4.4.0


# セットアップ手順

本プロジェクトをクローンもしくはダウンロードした後、以下のコマンドを実行する。

```cmd
$ cd twitter-list-generator
$ pip install -r requirements.txt
```

[Twitter Developers](https://developer.twitter.com/en/portal/dashboard)
で認証情報を発行する。
[発行手順](https://www.google.com/search?q=TwitterAPI+利用申請)
はググること。

`config/api_auth_info.json.sample`をコピペし、拡張子`.sample`を削除し、発行した認証情報を保存する。


# 使い方

リストに追加したいユーザ一覧のcsvファイルをinputフォルダに格納する。
その際にファイル名は作成したいリスト名にする。

また、フォーマットは当該フォルダ内のsampleファイルを参照する。

以下のコマンドを実行する。

```cmd
$ cd twitter-list-generator
$ py -m src
```


# 連絡先

[Twitter(@silverag_corgi)](https://twitter.com/silverag_corgi)


# ライセンス

MITライセンスの下で公開している。
詳細はLICENSEを確認すること。


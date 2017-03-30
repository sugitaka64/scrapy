# scrapy

## 概要

[SCP財団](http://ja.scp-wiki.net/)の記事をスクレイピングするツールです。

## 事前準備

MySQLをインストールし、テーブルを作成してください。

```sql
mysql> CREATE DATABASE scrapy;
mysql> USE scrapy;
mysql> CREATE TABLE scp (
    id INT NOT NULL AUTO_INCREMENT,
    item_no VARCHAR(16) NOT NULL,
    object_class VARCHAR(16) NOT NULL,
    protocol TEXT NOT NULL,
    description TEXT NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

```

本プログラムをcloneし、ライブラリをインストールしてください。

```shell-session
$ git clone https://github.com/sugitaka64/scrapy.git
$ cd scrapy
$ pip install -U -r requirements.txt
```

`get_scp/get_scp/pipelines.py`の13〜18行目にデータベースの設定を記載してください。

ログレベルの設定は`get_scp/get_scp/settings.py`の`LOG_LEVEL`を修正してください。
デフォルトでは`WARN`以上のログが標準出力に出力されます。

## 使用方法

```shell-session
$ cd /path/to/scrapy/get_scp/get_scp
$ scrapy crawl get_scp
```

上記テーブルにデータが格納されます。

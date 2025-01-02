# Wiki-Analyzer

Wiki-Analyzerは、Wikipediaのデータを取得し、そのデータを基にword2vecモデルを作成するプログラムです。このツールは、自然言語処理や機械学習の研究に役立ちます。

## セットアップ

以下の手順に従って、リポジトリをクローンし、必要なPythonパッケージをインストールしてください。

1. リポジトリをクローンする:

```bash
git clone https://github.com/XXXFQ/Wiki-Analyzer.git
cd Wiki-Analyzer
```

2. 必要なパッケージをインストールする:

```bash
pip install -r requirements.txt
```

## Wikipediaデータのダウンロード

以下のコマンドを実行して、最新の日本語版Wikipediaデータをダウンロードしてください。

```bash
curl https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2 -o jawiki-latest-pages-articles.xml.bz2
```

## ダンプデータから記事本文を抽出

以下のコマンドでダウンロードしたXMLデータを解凍し、記事本文を抽出します。

```bash
python -m wikiextractor.WikiExtractor jawiki-latest-pages-articles.xml.bz2
```

## 動作環境

* **Python**: 3.11.4

## 著作権表示

Copyright (C) 2025 ARM
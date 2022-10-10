# vnlpkit

Custom modules for Natural Language Processing

## Setup

### 1. Create .env

```sh
cp .env.template .env
```

### 2. Run JupyterLab

```sh
make up
```

## Download Corpus

### Download Livedoor News Corpus

次のノートブックを実行すると、[「livedoor ニュース」の記事データ](https://www.rondhuit.com/download.html)が `work/data/corpus/livedoor_news/livedoor_news_corpus_ldcc-20140209.csv` として保存されます。

work/data/corpus/notebooks/create_livedoor_news_corpus_dataset.ipynb

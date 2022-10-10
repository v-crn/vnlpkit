# 参考：[Livedoorニュースコーパスを文書分類にすぐ使えるように整形する - radiology-nlp’s blog](https://radiology-nlp.hatenablog.com/entry/2019/11/25/124219)

DATA_DIR=work/data/corpus/livedoor_news/raw
SOURCENAME=ldcc-20140209.tar.gz
SOURCEPATH=${DATA_DIR}/${SOURCENAME}
OUTPUT_FILENAME=livedoor_news_corpus_ldcc-20140209.tsv
FILEPATH=${DATA_DIR}/${OUTPUT_FILENAME}
TEXT_DIR=${DATA_DIR}/text

mkdir -p ${DATA_DIR}

# コーパスのダウンロード
wget https://www.rondhuit.com/download/ldcc-20140209.tar.gz -P ${DATA_DIR}
tar zxvf ${SOURCEPATH} -C ${DATA_DIR}

# ------------------------------------------------------------------
# 以下のコードを試してみたが、期待通りの形式で取得できなかった。
# そこで python でデータ整形を行うことにした。
# work/data/corpus/notebooks/create_livedoor_news_corpus_dataset.ipynb
# ------------------------------------------------------------------

# 各ニュース記事の ①ファイル名，②本文，③カテゴリのone-hot encoding を格納したtsvファイルを作成
# echo "filename\tarticle"$(for category in $(basename -a `find ${TEXT_DIR} -type d`\
#      | grep -v text | sort); do echo "\t"; echo $category; done) > ${FILEPATH}
# echo "filename\tarticle" $(for category in $(basename -a `find ${TEXT_DIR} -type d` | grep -v text | sort); do echo "\t"; echo $category; done) > ${FILEPATH}

# # 各ディレクトリ内のニュース記事の情報をtsvファイルに追記
# for filename in `basename -a ${TEXT_DIR}/dokujo-tsushin/dokujo-tsushin-*`; do echo "${filename}"; echo "\t"; echo `sed -e '1,3d' ${TEXT_DIR}/dokujo-tsushin/${filename}`; echo "\t1\t0\t0\t0\t0\t0\t0\t0\t0"; done >> ${FILEPATH}
# for filename in `basename -a ${TEXT_DIR}/it-life-hack/it-life-hack-*`; do echo "${filename}"; echo "\t"; echo `sed -e '1,3d' ${TEXT_DIR}/it-life-hack/${filename}`; echo "\t0\t1\t0\t0\t0\t0\t0\t0\t0"; done >> ${FILEPATH}
# for filename in `basename -a ${TEXT_DIR}/kaden-channel/kaden-channel-*`; do echo "${filename}"; echo "\t"; echo `sed -e '1,3d' ${TEXT_DIR}/kaden-channel/${filename}`; echo "\t0\t0\t1\t0\t0\t0\t0\t0\t0"; done >> ${FILEPATH}
# for filename in `basename -a ${TEXT_DIR}/livedoor-homme/livedoor-homme-*`; do echo "${filename}"; echo "\t"; echo `sed -e '1,3d' ${TEXT_DIR}/livedoor-homme/${filename}`; echo "\t0\t0\t0\t1\t0\t0\t0\t0\t0"; done >> ${FILEPATH}
# for filename in `basename -a ${TEXT_DIR}/movie-enter/movie-enter-*`; do echo "${filename}"; echo "\t"; echo `sed -e '1,3d' ${TEXT_DIR}/movie-enter/${filename}`; echo "\t0\t0\t0\t0\t1\t0\t0\t0\t0"; done >> ${FILEPATH}
# for filename in `basename -a ${TEXT_DIR}/peachy/peachy-*`; do echo "${filename}"; echo "\t"; echo `sed -e '1,3d' ${TEXT_DIR}/peachy/${filename}`; echo "\t0\t0\t0\t0\t0\t1\t0\t0\t0"; done >> ${FILEPATH}
# for filename in `basename -a ${TEXT_DIR}/smax/smax-*`; do echo "${filename}"; echo "\t"; echo `sed -e '1,3d' ${TEXT_DIR}/smax/${filename}`; echo "\t0\t0\t0\t0\t0\t0\t1\t0\t0"; done >> ${FILEPATH}
# for filename in `basename -a ${TEXT_DIR}/sports-watch/sports-watch-*`; do echo "${filename}"; echo "\t"; echo `sed -e '1,3d' ${TEXT_DIR}/sports-watch/${filename}`; echo "\t0\t0\t0\t0\t0\t0\t0\t1\t0"; done >> ${FILEPATH}
# for filename in `basename -a ${TEXT_DIR}/topic-news/topic-news-*`; do echo "${filename}"; echo "\t"; echo `sed -e '1,3d' ${TEXT_DIR}/topic-news/${filename}`; echo "\t0\t0\t0\t0\t0\t0\t0\t0\t1"; done >> ${FILEPATH}

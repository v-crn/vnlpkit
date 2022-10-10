import os

from work.config.path.general_dirs import GeneralDirs


class LivedoorNewsCorpusPaths:
    LIVEDOOR_NEWS_CORPUS_DIR = os.path.join(GeneralDirs.CORPUS_DIR, "livedoor_news")
    LIVEDOOR_NEWS_CORPUS_RAW_DIR = os.path.join(LIVEDOOR_NEWS_CORPUS_DIR, "raw")
    LIVEDOOR_NEWS_CORPUS_PRP_DIR = os.path.join(LIVEDOOR_NEWS_CORPUS_DIR, "processed")
    LIVEDOOR_NEWS_CORPUS_TEXT_DIR = os.path.join(LIVEDOOR_NEWS_CORPUS_DIR, "text")
    LIVEDOOR_NEWS_CORPUS_RAW_FILENAME = "livedoor_news_corpus_ldcc-20140209.csv"
    LIVEDOOR_NEWS_CORPUS_PRP_FILENAME = "livedoor_news_corpus_ldcc-20140209_prp.csv"
    LIVEDOOR_NEWS_CORPUS_RAW_PATH = os.path.join(
        LIVEDOOR_NEWS_CORPUS_RAW_DIR, LIVEDOOR_NEWS_CORPUS_RAW_FILENAME
    )
    LIVEDOOR_NEWS_CORPUS_PRP_PATH = os.path.join(
        LIVEDOOR_NEWS_CORPUS_PRP_DIR, LIVEDOOR_NEWS_CORPUS_PRP_FILENAME
    )

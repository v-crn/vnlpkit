from vnlpkit.utils.finder import find_path


class MecabDicPaths:
    MECAB_IPADIC_NEOLOGD_PATH = find_path(
        partial_path="mecab/dic/mecab-ipadic-neologd", use_cache=True
    )

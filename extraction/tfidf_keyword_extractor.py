import numpy as np
import pandas as pd
from typing import Iterable, Dict, List
from sklearn.feature_extraction.text import TfidfVectorizer
from utils import flatten


class TfIdfVectorizer(TfidfVectorizer):
    def __init__(self, n_docs: int = None):
        super().__init__(n_docs)
        self.n_docs = n_docs

    def first_fit(self, X):
        self.fit(X)
        self.n_docs = len(X)

    def partial_fit(self, X):
        from scipy.sparse import dia_matrix

        max_idx = max(self.vocabulary_.values())

        intervec = TfidfVectorizer(
            input=self.input,
            encoding=self.encoding,
            decode_error=self.decode_error,
            strip_accents=self.strip_accents,
            lowercase=self.lowercase,
            preprocessor=self.preprocessor,
            tokenizer=self.tokenizer,
            analyzer=self.analyzer,
            stop_words=self.stop_words,
            token_pattern=self.token_pattern,
            ngram_range=self.ngram_range,
            max_df=self.max_df,
            min_df=self.min_df,
            max_features=self.max_features,
            vocabulary=self.vocabulary,
            binary=self.binary,
            norm=self.norm,
            use_idf=self.use_idf,
            smooth_idf=self.smooth_idf,
            sublinear_tf=self.sublinear_tf
        )

        for a in X:
            # update vocabulary_
            if self.lowercase:
                a = a.lower()
            intervec.fit([a])
            tokens = intervec.get_feature_names()
            for w in tokens:
                if w not in self.vocabulary_:
                    max_idx += 1
                    self.vocabulary_[w] = max_idx

            # update idf_
            df = (self.n_docs + self.smooth_idf) / \
                np.exp(self.idf_ - 1) - self.smooth_idf
            self.n_docs += 1
            df.resize(len(self.vocabulary_), refcheck=False)
            for w in tokens:
                df[self.vocabulary_[w]] += 1
            idf = np.log((self.n_docs + self.smooth_idf) /
                         (df + self.smooth_idf)) + 1

            self._tfidf._idf_diag = dia_matrix(
                (idf, 0), shape=(len(idf), len(idf))
            )


class TfIdfKeywordExtractor(object):
    def __init__(
        self,
        input='content',
        encoding='utf-8',
        decode_error='strict',
        strip_accents=None,
        lowercase=True,
        preprocessor=None,
        tokenizer=None,
        analyzer='word',
        stop_words=None,
        token_pattern=r'(?u)\b\w\w+\b',
        ngram_range=(1, 1),
        max_df=1.0,
        min_df=0.03,
        max_features=None,
        freq_dict: Dict[str, int] = None,
        binary=False,
        norm='l2',
        use_idf=True,
        smooth_idf=True,
        sublinear_tf=False
    ):
        self.freq_dict = freq_dict
        self.vectorizer = TfIdfVectorizer(
            input=input,
            encoding=encoding,
            decode_error=decode_error,
            strip_accents=strip_accents,
            lowercase=lowercase,
            preprocessor=preprocessor,
            tokenizer=tokenizer,
            analyzer=analyzer,
            stop_words=stop_words,
            token_pattern=token_pattern,
            ngram_range=ngram_range,
            max_df=max_df,
            min_df=min_df,
            max_features=max_features,
            vocabulary=freq_dict,
            binary=binary,
            norm=norm,
            use_idf=use_idf,
            smooth_idf=smooth_idf,
            sublinear_tf=sublinear_tf
        )

    def set_freq_dict(self, raw_documents: Iterable) -> Dict[str, int]:
        if type(raw_documents) == str:
            raw_documents = [raw_documents]
        if (raw_documents == []) or not any(raw_documents):
            return
        self.vectorizer.fit(raw_documents)
        self.freq_dict = self.vectorizer.vocabulary_

    def update_freq_dict(self, raw_documents: Iterable) -> Dict[str, int]:
        if type(raw_documents) == str:
            raw_documents = [raw_documents]
        if (raw_documents == []) or not any(raw_documents):
            return
        self.vectorizer.partial_fit(raw_documents)
        self.freq_dict = self.vectorizer.vocabulary_

    def get_freq_dict(self, sort=False) -> Dict[str, int]:
        if sort:
            self.freq_dict = dict(
                sorted(
                    self.vectorizer.vocabulary_.items(),
                    key=lambda x: x[1], reverse=True
                )
            )
        return self.freq_dict

    def extract_keywords(
        self, documents: Iterable[str], n: int = None,
    ) -> List[str]:
        if (documents == []) or not any(documents):
            return []
        data = [documents] if type(documents) == str else documents
        if self.freq_dict is None:
            self.set_freq_dict(data)
        X = self.vectorizer.transform(data).toarray()
        index = X.argsort(axis=1)[:, ::-1]
        feature_names = np.array(self.vectorizer.get_feature_names())
        keywords = feature_names[index]
        if len(keywords) == 1:
            keywords = keywords[0]
            if n is None:
                return keywords.tolist()
            return keywords[:n].tolist()
        if n is None:
            return keywords.tolist()
        return keywords[:, :n].tolist()


def _extract_keywords_by_category(params):
    (
        df_category, text_col, n, extractor_params, keyword_col
    ) = params
    kw_extractor = TfIdfKeywordExtractor(**extractor_params)\
        if extractor_params is not None\
        else TfIdfKeywordExtractor()
    category_text = [c for c in set(flatten(df_category[text_col])) if c != '']
    kw_extractor.set_freq_dict(category_text)
    df_category[keyword_col] = df_category[text_col].apply(
        lambda x: kw_extractor.extract_keywords(
            documents=x,
            n=n
        )
    )
    return df_category


def add_tfidf_keyword_column(
    df: pd.DataFrame,
    category_col: str,
    text_col: str,
    n: int = None,
    extractor_params: dict = None,
    keyword_col: str = None
):
    import multiprocessing
    from concurrent.futures import ProcessPoolExecutor

    if keyword_col is None:
        keyword_col = f'tfidf_keyword_of_{text_col}'

    df = df.copy()
    categories = df[category_col].unique()
    params_list = [
        (
            df[df[category_col] == category],
            text_col, n, extractor_params, keyword_col
        )
        for category in categories
    ]

    max_workers = multiprocessing.cpu_count()
    with ProcessPoolExecutor(max_workers) as executor:
        df_categories = list(
            executor.map(_extract_keywords_by_category, params_list)
        )

    return pd.concat(df_categories)


def add_tfidf_combined_keyword_column(
    df, category_col: str,
    main_text_col: str,
    sub_text_mapping: Dict[str, int],
    n: int,
    extractor_params: dict = None,
    keyword_col: str = None
):
    def combine_keywords(
        x: pd.Series,
        main_keyword_col: str,
        sub_keyword_cols: List[str],
        n: int = None
    ) -> List[str]:
        keywords = []
        if n is None:
            n = len(x[main_keyword_col])
        n_main_keywords = n
        for sub_keyword_col in sub_keyword_cols:
            keywords.extend(x[sub_keyword_col])
            n_main_keywords -= len(x[sub_keyword_col])
        keywords.extend(x[main_keyword_col][:n_main_keywords])
        return keywords

    main_keyword_col = '_main_keyword'
    df = df.copy()
    df = add_tfidf_keyword_column(
        df=df,
        category_col=category_col,
        text_col=main_text_col,
        n=n,
        extractor_params=extractor_params,
        keyword_col=main_keyword_col
    )
    sub_keyword_cols = []
    for sub_text_col, n_sub_keywords in sub_text_mapping.items():
        sub_keyword_col = f'_sub_keyword_{sub_text_col}'
        sub_keyword_cols.append(sub_keyword_col)
        df = add_tfidf_keyword_column(
            df=df,
            category_col=category_col,
            text_col=sub_text_col,
            n=n_sub_keywords,
            extractor_params=extractor_params,
            keyword_col=sub_keyword_col
        )
    cols = [main_keyword_col] + sub_keyword_cols

    if keyword_col is None:
        sub_text_cols = [
            str(sub_text_col) for sub_text_col in sub_text_mapping.keys()
        ]
        sub_text_cols_name = '_'.join(sub_text_cols)
        keyword_col = 'tfidf_combined_keyword_of'\
            f'_{main_text_col}_{sub_text_cols_name}'

    df[keyword_col] = ''
    df[keyword_col] = df[cols].apply(
        lambda x: combine_keywords(
            x, main_keyword_col=main_keyword_col,
            sub_keyword_cols=sub_keyword_cols,
            n=n
        ), axis=1
    )
    df.drop(cols, axis=1, inplace=True)
    return df


def count_word_frequency(
    words: List[str], freq_dict: Dict[str, int] = None
):
    from collections import Counter

    counter = Counter(freq_dict)
    counter.update(words)
    return dict(counter)

import os
import collections
import termextract
import termextract.core
import termextract.japanese_plaintext
import janome
import MeCab
import dbm


def calc_term_imp(
        frequency, metric: str = 'score_pp',
        average_rate: float = 1.0, lr_mode: int = 1):
    if metric == 'score_pp':
        term_imp = termextract.core.score_pp(
            frequency,
            ignore_words=termextract.mecab.IGNORE_WORDS,
            average_rate=average_rate)
    elif metric == 'score_lr':
        lr = termextract.core.score_lr(
            frequency, ignore_words=termextract.mecab.IGNORE_WORDS,
            average_rate=average_rate,
            lr_mode=lr_mode, dbm=None)
        term_imp = termextract.core.term_importance(frequency, lr)
    elif metric == 'tf_idf':
        # 頻度辞書ファイル作成
        DF = dbm.open("./tmp/tf_idf_df", "n")
        termextract.core.store_df(frequency, dbm=DF)
        tf = termextract.core.frequency2tf(frequency)
        idf = termextract.core.get_idf(frequency, dbm=DF)
        DF.close()
        # 頻度辞書ファイル削除
        filepath_to_remove = [
            './tmp/tf_idf_df.bak', './tmp/tf_idf_df.dat', './tmp/tf_idf_df.dir'
        ]
        for path in filepath_to_remove:
            os.remove(path)

        # 重要度をTFとIDFの組み合わせとし、ファイル出力
        term_imp = termextract.core.term_importance(tf, idf)
    return term_imp


def extract_kw_by_termextract(
        text, upper=None, return_type='with_score', dic=None,
        morph_analyzer='mecab', metrics='score_pp',
        average_rate: float = 1.0, lr_mode: int = 1):
    if morph_analyzer == 'janome':
        t = janome.tokenizer.Tokenizer()
        tokens = t.tokenize(text)
        frequency = termextract.janome.cmp_noun_dict(tokens)
    elif morph_analyzer == 'mecab':
        wakati = MeCab.Tagger() if dic is None \
            else MeCab.Tagger(f"-d {dic}")
        tokens = wakati.parse(text)
        frequency = termextract.mecab.cmp_noun_dict(tokens)
    elif morph_analyzer == 'japanese_nouns':
        frequency = termextract.japanese_plaintext.cmp_noun_dict(text)
    elif morph_analyzer == 'english_nouns':
        frequency = termextract.english_plaintext.cmp_noun_dict(text)
    elif morph_analyzer == 'chinese_nouns':
        frequency = termextract.chinese_plaintext.cmp_noun_dict(text)

    if type(metrics) == str:
        term_imp = calc_term_imp(
            frequency, metrics,
            average_rate=average_rate, lr_mode=lr_mode)
    elif type(metrics) == list:
        term_imps = [calc_term_imp(frequency, metric) for metric in metrics]
        term_imp = termextract.core.term_importance(term_imps)

    data_collection = collections.Counter(term_imp)
    output = {
        cmp_noun: value for cmp_noun, value
        in data_collection.most_common()
    }
    if type(upper) == int:
        if upper > len(output):
            upper = len(output)
        output = {k: output[k] for k in list(output)[:upper]}
    if return_type == 'with_score':
        return output
    output = [k for k in output.keys()]
    if return_type == 'str':
        return ' '.join(output)
    return output

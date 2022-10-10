import pandas as pd
from tqdm import tqdm


def load_lang_model(path_w2v, path_swem):
    import os

    import swem
    from gensim.models.word2vec import Word2Vec
    from utils.load_and_dump import dump_with_cloudpickle, load_with_cloudpickle

    if os.path.exists(path_swem):
        return load_with_cloudpickle(path_swem)

    w2v = Word2Vec.load(path_w2v)
    lang_model = swem.SWEM(w2v, lang="ja")
    dump_with_cloudpickle(lang_model, path_swem)
    return lang_model


def create_columns_from_nested_array(df, col):
    return df.join(pd.DataFrame(df[col].tolist(), index=df.index).add_prefix(col + "_"))


def vectorize_with_swem(lang_model, df, text_cols, method="max"):
    """A main method to get document vector
    Args:
        lang_model: SWEM model.
        method (str): Designate method to pool.
                     ('max', 'avg', 'concat', 'hierarchical')
    Returns:
        pandas.DataFrame
    """
    for col in tqdm(text_cols):
        df_vec = pd.DataFrame(
            df[col].apply(lambda x: lang_model.infer_vector(x, method=method))
        )
        df_ = create_columns_from_nested_array(df_vec, col)
        df = pd.concat([df, df_], axis=1)
        df.drop(col, axis=1, inplace=True)
    return df

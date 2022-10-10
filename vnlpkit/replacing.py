import re

from googletrans import Translator


def replace_with_single_separator(orginal_separator: str, separator: str, text: str):
    return re.sub(
        separator + "+", separator, text.replace(orginal_separator, separator)
    )


def translate_column_names_with_googletrans(df, src="ja", dest="en"):
    # Caution! googletrans を使いすぎると API の制約で JSONDecodeError になる
    translator = Translator()

    cols = df.columns
    trans_dict = {}

    for col in cols:
        col_translated = translator.translate(col, src=src, dest=dest).text
        col_translated = replace_with_single_separator(" ", "_", col_translated)
        trans_dict[col] = col_translated
    df.rename(columns=trans_dict)
    return df


def rename_columns(df, cols_translated):
    cols = df.columns
    trans_dict = {}

    for i, col in enumerate(cols):
        cols_translated[i] = cols_translated[i].replace(" ", "_")
        cols_translated[i] = cols_translated[i].replace("__", "_")
        trans_dict[col] = cols_translated[i]
    df = df.rename(columns=trans_dict)
    return df

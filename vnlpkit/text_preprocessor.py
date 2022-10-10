import re
import unicodedata
from typing import Iterable

import demoji
import neologdn
import numpy as np
from tqdm.auto import tqdm

tqdm.pandas()


class TextPreprocessor:
    def __init__(
        self,
        use_neologdn: bool = True,
        remove_url: bool = True,
        remove_emoji: bool = True,
        remove_thousand_separator: bool = True,
        replace_digit: bool = False,
        remove_full_width_symbol: bool = True,
        remove_half_width_symbol: bool = True,
        use_unicode_normalization: bool = True,
    ) -> None:
        self.use_neologdn = use_neologdn
        self.remove_url = remove_url
        self.remove_emoji = remove_emoji
        self.remove_thousand_separator = remove_thousand_separator
        self.replace_digit = replace_digit
        self.remove_full_width_symbol = remove_full_width_symbol
        self.remove_half_width_symbol = remove_half_width_symbol
        self.use_unicode_normalization = use_unicode_normalization

    def run(
        self,
        text: str,
        use_neologdn: bool = True,
        remove_url: bool = True,
        remove_emoji: bool = True,
        remove_thousand_separator: bool = True,
        replace_digit: bool = False,
        remove_full_width_symbol: bool = True,
        remove_half_width_symbol: bool = True,
        use_unicode_normalization: bool = True,
    ) -> str:
        self.use_neologdn = use_neologdn
        self.remove_url = remove_url
        self.remove_emoji = remove_emoji
        self.remove_thousand_separator = remove_thousand_separator
        self.replace_digit = replace_digit
        self.remove_full_width_symbol = remove_full_width_symbol
        self.remove_half_width_symbol = remove_half_width_symbol
        self.use_unicode_normalization = use_unicode_normalization

        # URL の削除（空白文字に置換）
        # [Note] `separator` の前後に空白文字がないと、separator も URL の一部と見做されて消されることがあるので注意
        if self.remove_url:
            regex = (
                r"(https?|ftp?|http?)(:\/\/[-_\.!~*\’()a-zA-Z0-9;\/?:\@ &=\+\$,%#]+)"
            )
            text = re.sub(regex, " ", text)

        # 絵文字の削除（空白文字に置換）
        if remove_emoji:
            text = demoji.replace(string=text, repl=" ")

        # 数字の桁区切り記号 (,) の削除
        if remove_thousand_separator:
            text = re.sub(r"(\d)([,.])(\d+)", r"\1\3", text)

        # 数字を '0' に置換
        if replace_digit:
            text = re.sub(r"\d+", "0", text)

        # 半角記号を削除
        if remove_half_width_symbol:
            text = re.sub(r"[!-/:-@[-`{-~]", " ", text)

        # 全角記号を削除（ここでは 0x25A0 - 0x266F のブロックのみを削除）
        if remove_full_width_symbol:
            text = re.sub("[■-♯]", " ", text)

        # 全角・半角の統一と重ね表現の削除
        if self.use_neologdn:
            text = neologdn.normalize(text)

        # Unicode 正規化
        if use_unicode_normalization:
            text = unicodedata.normalize("NFKC", text)

        return text

    def run_all(
        self,
        documents: Iterable[str],
        use_neologdn: bool = True,
        remove_url: bool = True,
        remove_emoji: bool = True,
        remove_thousand_separator: bool = True,
        replace_digit: bool = False,
        remove_full_width_symbol: bool = True,
        remove_half_width_symbol: bool = True,
        use_unicode_normalization: bool = True,
    ) -> list[str]:
        def _func(text: str, pbar) -> list[str]:
            filtered_text = self.run(
                text,
                use_neologdn=use_neologdn,
                remove_url=remove_url,
                remove_emoji=remove_emoji,
                remove_thousand_separator=remove_thousand_separator,
                replace_digit=replace_digit,
                remove_full_width_symbol=remove_full_width_symbol,
                remove_half_width_symbol=remove_half_width_symbol,
                use_unicode_normalization=use_unicode_normalization,
            )
            pbar.update(1)
            return filtered_text

        with tqdm(total=len(documents)) as pbar:
            filtered_documents = np.vectorize(_func)(documents, pbar)

        return filtered_documents

    def run_all_with_sep(
        self,
        documents: Iterable[str],
        separator: str = "üßäö",
        use_neologdn: bool = True,
        remove_url: bool = True,
        remove_emoji: bool = True,
        remove_thousand_separator: bool = True,
        replace_digit: bool = False,
        remove_full_width_symbol: bool = True,
        remove_half_width_symbol: bool = True,
        use_unicode_normalization: bool = True,
    ) -> list[str]:
        """
        `run_all_with_sep()` は `run_all()` よりも高速ですが、データによってはうまく separator が機能しないことがあります。
        適切な separator を見つけるのが難しい場合、 `run_all()` の使用を推奨します。
        """
        tmp_separator = separator
        text: str = tmp_separator.join(documents)
        filtered_documents_text = self.run(
            text,
            use_neologdn=use_neologdn,
            remove_url=remove_url,
            remove_emoji=remove_emoji,
            remove_thousand_separator=remove_thousand_separator,
            replace_digit=replace_digit,
            remove_full_width_symbol=remove_full_width_symbol,
            remove_half_width_symbol=remove_half_width_symbol,
            use_unicode_normalization=use_unicode_normalization,
        )
        filtered_documents = filtered_documents_text.split(separator)
        # diff = len(documents) - len(filtered_documents)
        # assert diff == 0, f"documents length must be equal to filtered_documents. \ndiff: {diff}"

        return filtered_documents

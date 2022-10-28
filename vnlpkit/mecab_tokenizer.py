import re
from typing import List, Optional
import unicodedata

import MeCab
import numpy as np
from tqdm.auto import tqdm

tqdm.pandas()


class MecabTokenizer:
    def __init__(
        self,
        dict_path: Optional[str] = None,
    ) -> None:
        self.tagger = (
            MeCab.Tagger() if dict_path is None else MeCab.Tagger(f"-d {dict_path}")
        )
        self.kana_re = re.compile("^[ぁ-ゖ]+$")
        self.stop_words = None

    def run(
        self,
        text: str,
        target_pos_0_list: Optional[List[str]] = ["名詞", "動詞", "形容詞"],
        without_pos_1_list: Optional[List[str]] = ["代名詞", "接尾", "非自立"],
        remove_hiragana_only: bool = False,
        lower_letter_case: bool = True,
        stop_words: Optional[List[str]] = None,
    ) -> str:
        self.stop_words = stop_words if stop_words is not None else []
        target_pos_0_list = [] if target_pos_0_list is None else target_pos_0_list
        without_pos_1_list = [] if without_pos_1_list is None else without_pos_1_list

        # 分かち書き
        parsed_text = self.tagger.parse(text)
        parsed_lines = parsed_text.split("\n")[:-2]
        token_list = []

        for parsed_line in parsed_lines:
            surface = parsed_line.split("\t")[0]

            # 品詞
            feature = parsed_line.split("\t")[1]

            # 原型を取得
            base = feature.split(",")[6]

            # Token を取得
            token = base if base != "*" else surface

            # 品詞の絞り込み
            pos_0 = feature.split(",")[0]
            pos_1 = feature.split(",")[1]

            if pos_0 not in target_pos_0_list:
                continue

            if pos_1 in without_pos_1_list:
                continue

            # stopwords に含まれていれば除去
            if token in self.stop_words:
                continue

            # ひらがなのみの単語を除く
            if remove_hiragana_only and self.kana_re.match(token):
                continue

            # アルファベットを小文字に統一
            token = token.lower() if lower_letter_case else token

            token_list.append(token)

        tokenized_text = " ".join(token_list)

        # Unicode 正規化
        tokenized_text = unicodedata.normalize("NFKC", tokenized_text)

        return tokenized_text

    def run_all(
        self,
        documents: list[str],
        target_pos_0_list: Optional[List[str]] = ["名詞", "動詞", "形容詞"],
        without_pos_1_list: Optional[List[str]] = ["代名詞", "接尾", "非自立"],
        remove_hiragana_only: bool = False,
        lower_letter_case: bool = True,
        stop_words: Optional[List[str]] = None,
    ) -> list[str]:
        def _func(text: str, pbar) -> list[str]:
            tokenized_text = self.run(
                text,
                target_pos_0_list=target_pos_0_list,
                without_pos_1_list=without_pos_1_list,
                remove_hiragana_only=remove_hiragana_only,
                lower_letter_case=lower_letter_case,
                stop_words=stop_words,
            )
            pbar.update(1)
            return tokenized_text

        with tqdm(total=len(documents)) as pbar:
            tokenized_documents = np.vectorize(_func)(documents, pbar)

        return tokenized_documents

    def run_all_with_sep(
        self,
        documents: list[str],
        separator: str = "üßäö",
        target_pos_0_list: Optional[List[str]] = ["名詞", "動詞", "形容詞"],
        remove_hiragana_only: bool = False,
        lower_letter_case: bool = True,
        stop_words: Optional[List[str]] = None,
    ) -> list[str]:
        """
        `run_all_with_sep()` は `run_all()` よりも高速ですが、データによってはうまく separator が機能しないことがあります。
        適切な separator を見つけるのが難しい場合、 `run_all()` の使用を推奨します。
        """
        tmp_separator = separator
        text = tmp_separator.join(documents)
        tokenized_documents_text = self.run(
            text,
            target_pos_0_list=target_pos_0_list,
            remove_hiragana_only=remove_hiragana_only,
            lower_letter_case=lower_letter_case,
            stop_words=stop_words,
        )
        tokenized_documents = tokenized_documents_text.split(separator)
        # diff = len(documents) - len(tokenized_documents)
        # assert diff == 0, f"documents length must be equal to filtered_documents. \ndiff: {diff}"

        return tokenized_documents

import re
import unicodedata

import MeCab
import numpy as np
from tqdm.auto import tqdm

tqdm.pandas()


class MecabTokenizer:
    def __init__(
        self,
        dict_path: str | None = None,
    ) -> None:
        self.tagger = (
            MeCab.Tagger() if dict_path is None else MeCab.Tagger(f"-d {dict_path}")
        )
        self.kana_re = re.compile("^[ぁ-ゖ]+$")
        self.stop_words = None

    def run(
        self,
        text: str,
        target_pos_list: list[str] | None = ["名詞", "動詞", "形容詞"],
        remove_hiragana_only: bool = False,
        lower_letter_case: bool = True,
        stop_words: list[str] | None = None,
    ) -> str:
        self.stop_words = stop_words if stop_words is not None else []

        # 分かち書き
        parsed_text = self.tagger.parse(text)
        parsed_lines = parsed_text.split("\n")[:-2]
        surfaces = [l.split("\t")[0] for l in parsed_lines]
        features = [l.split("\t")[1] for l in parsed_lines]

        # 原型を取得
        bases = [f.split(",")[6] for f in features]

        # 各単語を原型に変換する
        token_list = [b if b != "*" else s for s, b in zip(surfaces, bases)]

        # 品詞の絞り込み
        if (target_pos_list is not None) and (len(target_pos_list) > 0):
            pos = [f.split(",")[0] for f in features]
            token_list = [t for t, p in zip(token_list, pos) if (p in target_pos_list)]

        _token_list = []
        for token in token_list:
            # stopwords に含まれていれば除去
            if token in self.stop_words:
                continue

            # ひらがなのみの単語を除く
            if remove_hiragana_only and self.kana_re.match(token):
                continue

            # アルファベットを小文字に統一
            token = token.lower() if lower_letter_case else token

            _token_list.append(token)

        # 半角スペースを挟んで結合
        tokenized_text = " ".join(_token_list)

        # 再度ユニコード正規化
        tokenized_text = unicodedata.normalize("NFKC", tokenized_text)

        return tokenized_text

    def run_all(
        self,
        documents: list[str],
        target_pos_list: list[str] | None = ["名詞", "動詞", "形容詞"],
        remove_hiragana_only: bool = False,
        lower_letter_case: bool = True,
        stop_words: list[str] | None = None,
    ) -> list[str]:
        def _func(text: str, pbar) -> list[str]:
            tokenized_text = self.run(
                text,
                target_pos_list=target_pos_list,
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
        target_pos_list: list[str] | None = ["名詞", "動詞", "形容詞"],
        remove_hiragana_only: bool = False,
        lower_letter_case: bool = True,
        stop_words: list[str] | None = None,
    ) -> list[str]:
        """
        `run_all_with_sep()` は `run_all()` よりも高速ですが、データによってはうまく separator が機能しないことがあります。
        適切な separator を見つけるのが難しい場合、 `run_all()` の使用を推奨します。
        """
        tmp_separator = separator
        text = tmp_separator.join(documents)
        tokenized_documents_text = self.run(
            text,
            target_pos_list=target_pos_list,
            remove_hiragana_only=remove_hiragana_only,
            lower_letter_case=lower_letter_case,
            stop_words=stop_words,
        )
        tokenized_documents = tokenized_documents_text.split(separator)
        # diff = len(documents) - len(tokenized_documents)
        # assert diff == 0, f"documents length must be equal to filtered_documents. \ndiff: {diff}"

        return tokenized_documents

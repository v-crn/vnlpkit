import re
import emoji


class EOSPhraseFilter(object):
    """
    テキストから抽出したフレーズを list に格納し、前方から指定の割合だけ取り出して空白区切りのテキストとして返す。
    """

    def __init__(self, copy=True, upper_size=1.0):
        super().__init__(copy)
        self.upper_size = upper_size

        # フレーズ区切り文字
        self.eos_pattern = re.compile(
            r"[\n@←→↑↓♪♫♬♥♡▲△▼▽★☆■□◆◇●○。.!！?？？!/\|#＃:interrobang::…-]"
        )
        self.replacement = ""

    def apply(self, text):
        upper_size = self.upper_size

        # 注釈 -> 削除
        note = re.compile(r"\※(.*?)\。")
        text = note.sub("", text)
        # 記号 -> 削除
        symbol = re.compile(r"♪|♫|♬|♡|♥|△|▼|☆|■|◆")
        text = symbol.sub("", text)
        # 括弧で括られた文字
        utter = re.compile(r"\「(.*?)\」")
        utters = utter.search(text)
        text = utter.sub("", text)
        # 括弧 -> 削除
        bracket = re.compile(r"【|】|<|>|＜|＞|『|』|「|」")
        brackets = bracket.search(text)
        text = bracket.sub("", text)
        # スラッシュで括られた文字
        slash = re.compile(r"\＼(.*?)\／")
        slashs = slash.search(text)
        text = slash.sub("", text)
        # 日本語
        jp = re.compile(r"[ぁ-んァ-ン]")
        # 文字化け -> 削除
        unk = re.compile("�")
        text = unk.sub("", text)
        # 全角スペース
        uni_space = re.compile("\u3000")
        text = uni_space.sub("", text)
        # ハッシュタグ
        hashtag = re.compile(r"  # (\w+)")
        text = hashtag.sub("", text)
        # URL削除
        url = re.compile(
            r"""
            (https?| ftp | http)
            (: \/\/[-_\.!~*\’()a-zA-Z0-9; \/?:\@ &=\+\$, %  # ]+)
            """
        )
        text = url.sub("", text)
        # 絵文字の削除
        text = "".join([
            w if w not in emoji.UNICODE_EMOJI else "。"
            for w in text
        ])

        # フレーズの抽出
        phrases = [p for p in self.eos_pattern.split(text) if p != ""]
        # 発話、括弧、スラッシュに囲われたものの抽出
        if utters:
            phrases += list(utters.groups())
        if brackets:
            phrases += list(brackets.groups())
        if slashs:
            phrases += list(slashs.groups())
        phrases = [p for p in phrases if jp.findall(p)]

        # フレーズ区切り文字の削除
        phrases = [self.eos_pattern.sub("", p) for p in phrases]

        # 重複の削除
        phrases = list(set(phrases))

        if type(upper_size) == float:
            n_upper_phrases = int(len(phrases) * upper_size)
        elif type(upper_size) == int:
            n_upper_phrases = upper_size
        else:
            raise ValueError("upper_size must be float or int.")
        return ' '.join(phrases[:n_upper_phrases])

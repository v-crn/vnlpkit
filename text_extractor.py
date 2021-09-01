import re


class InsideBracketsExtractor(object):
    """
    括弧で挟まれた文字列を抽出する。
    """

    def __init__(
            self, copy=True,
            pattern=r"[【《＼＜\[(「『](.*?)[】》／＞\])」』]",
            return_type='str'
    ):
        super().__init__(copy)
        self._regex = re.compile(pattern)
        self.return_type = return_type

    def apply(self, text):
        text_list = self._regex.findall(text)
        if self.return_type == 'str':
            return text_list
        return ' '.join(text_list)

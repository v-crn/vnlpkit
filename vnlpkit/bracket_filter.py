import re


class BracketFilter(object):
    def __init__(
        self,
        copy=True,
        pattern=r"【|】|《|》|＼|／|<|>|＜|＞|『|』|「|」",
    ):
        super().__init__(copy)
        self.pattern = pattern
        self.replacement = ""

    def apply(self, text):
        return re.sub(self.pattern, self.replacement, text)

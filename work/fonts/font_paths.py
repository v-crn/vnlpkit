from vnlpkit.utils.finder import find_path


class FontPaths:
    # IPAEXG_PATH = find_path(partial_path="ipaexg.ttf", use_cache=True)
    NOTO_SANS_CJK_REGULAR_PATH = find_path(
        partial_path="NotoSansCJK-Regular.ttc", use_cache=True
    )
    NOTO_SANS_CJK_BOLD_PATH = find_path(
        partial_path="NotoSansCJK-Bold.ttc", use_cache=True
    )
    NOTO_SERIF_CJK_REGULAR_PATH = find_path(
        partial_path="NotoSerifCJK-Regular.ttc", use_cache=True
    )

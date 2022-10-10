from typing import Dict, List


def count_word_frequency(words: List[str], freq_dict: Dict[str, int] = None):
    from collections import Counter

    counter = Counter(freq_dict)
    counter.update(words)
    return dict(counter)

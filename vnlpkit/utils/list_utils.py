def drop_duplicates_for_list(l):
    return list(set(l))


def get_idx_matched_value(lst, value):
    return [idx for idx, v in enumerate(lst) if v == value]


def get_values_matched_idx(lst, idx_list):
    return [lst[i] for i in idx_list]


def bool2binary(lst):
    return [1 if x else 0 for x in lst]


def uniq(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if x not in seen and not seen_add(x)]


def intersect(lst):
    return list(set(lst[0]).intersection(*lst[1:]))


def flatten(lst: list):
    return [
        z
        for y in lst
        for z in (
            flatten(y) if hasattr(y, "__iter__") and not isinstance(y, str) else (y,)
        )
    ]

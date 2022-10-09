
from vnlpkit.utils.finder import find_path
import time

def test_find_path__cache_is_faster() -> None:
    partial_path = "test_finder.py"

    start_time = time.time()
    filepath = find_path(partial_path=partial_path, use_cache=False)
    without_cache_time = time.time() - start_time

    start_time = time.time()
    find_path(partial_path=partial_path, use_cache=True)
    with_cache_time_1 = time.time() - start_time
    diff_without_cache_time_and_with_cache_time_1 = without_cache_time - with_cache_time_1

    start_time = time.time()
    find_path(partial_path=partial_path, use_cache=True)
    with_cache_time_2 = time.time() - start_time
    diff_without_cache_time_and_with_cache_time_2 = without_cache_time - with_cache_time_2

    print()
    print(f"Found filepath: {filepath}")
    print()
    print("--- Result ---")
    print(f"without_cache_time: {without_cache_time}")
    print(f"with_cache_time_1: {with_cache_time_1}")
    print(f"with_cache_time_2: {with_cache_time_2}")
    print(f"diff_without_cache_time_and_with_cache_time_1: {diff_without_cache_time_and_with_cache_time_1}")
    print(f"diff_without_cache_time_and_with_cache_time_2: {diff_without_cache_time_and_with_cache_time_2}")

    assert with_cache_time_1 > with_cache_time_2

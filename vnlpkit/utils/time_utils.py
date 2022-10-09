import time
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def timer(name: str = "process") -> Iterator[None]:
    """
    Usage:
        with timer('process train'):
            (Process)
    """
    print(f"\n[{name}] start\n")
    start_time = time.time()
    yield
    print(f"\n[{name}] done in {time.time() - start_time:.2f} sec\n")

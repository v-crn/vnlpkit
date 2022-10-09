import subprocess
from functools import cache


@cache
def _find_path(
    partial_path: str,
    target_dir: str = "/",
) -> str:
    cmd = f"find {target_dir} -path */{partial_path} 2> /dev/null | head -1"
    return (
        subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            encoding="utf-8",
        )
        .communicate()[0]
        .strip()
    )


def find_path(
    partial_path: str,
    target_dir: str = "/",
    use_cache: bool = False,
) -> str:
    if use_cache:
        return _find_path(partial_path=partial_path, target_dir=target_dir)

    return _find_path.__wrapped__(partial_path=partial_path, target_dir=target_dir)

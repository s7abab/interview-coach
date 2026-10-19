from pathlib import Path

import pytest


def pytest_configure(config: pytest.Config) -> None:
    tests_dir = (config.rootpath / "tests").resolve()
    src_dir = (config.rootpath / "src").resolve()
    if not tests_dir.is_dir():
        return

    invocation_dir = config.invocation_params.dir.resolve()
    resolved_args = [
        (Path(arg) if Path(arg).is_absolute() else invocation_dir / arg).resolve()
        for arg in config.args
    ]
    if resolved_args and all(
        path.is_dir() and (path == src_dir or src_dir in path.parents)
        for path in resolved_args
    ):
        config.args[:] = [str(tests_dir)]

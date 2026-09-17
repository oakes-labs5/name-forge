"""Loading word lists from wherever they happen to live."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable, Iterator, TextIO, Union

# A source is a file path, an already-open file-like object, or nothing/"-"
# meaning "read from stdin". Accepting all three means a WordBank can be
# built the same way whether the words come from a checked-in file or from
# a shell pipeline (e.g. `grep ... names.txt | some_script.py`).
Source = Union[str, Path, TextIO, None]


def read_words(source: Source = None) -> list[str]:
    """Read one word per line from a path, an open file, or stdin.

    Blank lines and lines starting with '#' are skipped so word list files
    can carry comments the same way a requirements file would.
    """
    if source is None or source == "-":
        return list(_clean_lines(sys.stdin))
    if hasattr(source, "read"):
        return list(_clean_lines(source))
    path = Path(source)
    with path.open("r", encoding="utf-8") as handle:
        return list(_clean_lines(handle))


def _clean_lines(handle: Iterable[str]) -> Iterator[str]:
    for raw_line in handle:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        yield line

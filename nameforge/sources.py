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
    return list(_source_lines(source))


def read_weighted_words(source: Source = None) -> list[tuple[str, float]]:
    """Read words with optional weights, one per line.

    Each line is either `word` or `word weight`, where weight is a positive
    number. A line with no weight gets 1.0, so an existing plain word list
    can be pointed at this function without editing every line.
    """
    return [_parse_weight(line) for line in _source_lines(source)]


def _parse_weight(line: str) -> tuple[str, float]:
    word, sep, weight_str = line.rpartition(" ")
    if not sep:
        return line, 1.0
    try:
        weight = float(weight_str)
    except ValueError:
        return line, 1.0
    if weight <= 0:
        raise ValueError(f"weight must be positive: {line!r}")
    return word, weight


def _source_lines(source: Source) -> Iterator[str]:
    if source is None or source == "-":
        yield from _clean_lines(sys.stdin)
        return
    if hasattr(source, "read"):
        yield from _clean_lines(source)
        return
    path = Path(source)
    with path.open("r", encoding="utf-8") as handle:
        yield from _clean_lines(handle)


def _clean_lines(handle: Iterable[str]) -> Iterator[str]:
    for raw_line in handle:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        yield line

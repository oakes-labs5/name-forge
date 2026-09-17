"""Building random names out of word banks and a template."""

from __future__ import annotations

import random
from typing import Optional, Sequence

from .sources import Source, read_words


class WordBank:
    """The candidate words for one slot in a name template."""

    def __init__(self, words: Sequence[str]):
        words = list(words)
        if not words:
            raise ValueError("word bank cannot be empty")
        self._words = words

    @classmethod
    def from_source(cls, source: Source = None) -> "WordBank":
        """Build a bank from a file path, an open file, or stdin.

        Passing no argument (or "-") reads stdin, so a bank can be piped in
        without the caller needing a separate stdin-handling code path.
        """
        return cls(read_words(source))

    def choice(self, rng: random.Random) -> str:
        return rng.choice(self._words)

    def __len__(self) -> int:
        return len(self._words)


class NameGenerator:
    """Fills a template string with random picks from named word banks.

    Example:
        adjectives = WordBank(["quiet", "loud"])
        nouns = WordBank(["river", "hill"])
        gen = NameGenerator("{adjective}-{noun}", adjective=adjectives, noun=nouns)
        gen.generate()  # "quiet-hill", "loud-river", ...
    """

    def __init__(self, template: str, **banks: WordBank):
        if not banks:
            raise ValueError("at least one word bank is required")
        self._template = template
        self._banks = banks

    def generate(self, rng: Optional[random.Random] = None) -> str:
        rng = rng or random.Random()
        values = {name: bank.choice(rng) for name, bank in self._banks.items()}
        return self._template.format(**values)

    def generate_many(self, count: int, rng: Optional[random.Random] = None) -> list[str]:
        rng = rng or random.Random()
        return [self.generate(rng) for _ in range(count)]

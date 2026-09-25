"""Building random names out of word banks and a template."""

from __future__ import annotations

import random
from typing import Optional, Sequence

from .sources import Source, read_weighted_words, read_words


class WordBank:
    """The candidate words for one slot in a name template.

    Words are picked with equal odds unless weights are given, in which
    case heavier words come up more often (a weight of 2 is twice as
    likely as a weight of 1). Weights don't need to sum to anything in
    particular; only the ratios between them matter.
    """

    def __init__(self, words: Sequence[str], weights: Optional[Sequence[float]] = None):
        words = list(words)
        if not words:
            raise ValueError("word bank cannot be empty")
        if weights is not None:
            weights = list(weights)
            if len(weights) != len(words):
                raise ValueError("weights must have the same length as words")
            if any(weight <= 0 for weight in weights):
                raise ValueError("weights must be positive")
        self._words = words
        self._weights = weights

    @classmethod
    def from_source(cls, source: Source = None) -> "WordBank":
        """Build a bank from a file path, an open file, or stdin.

        Passing no argument (or "-") reads stdin, so a bank can be piped in
        without the caller needing a separate stdin-handling code path.
        """
        return cls(read_words(source))

    @classmethod
    def from_weighted_source(cls, source: Source = None) -> "WordBank":
        """Like `from_source`, but each line may carry a trailing weight.

        A line is either `word` or `word weight`, e.g. `common 5`. Lines
        without a weight default to 1.0, so a plain word list works here
        too, just without any bias.
        """
        pairs = read_weighted_words(source)
        words = [word for word, _ in pairs]
        weights = [weight for _, weight in pairs]
        return cls(words, weights)

    def choice(self, rng: random.Random) -> str:
        if self._weights is None:
            return rng.choice(self._words)
        return rng.choices(self._words, weights=self._weights, k=1)[0]

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

# nameforge

A small library for generating random names by filling a template with
words picked from one or more lists. No CLI, no framework, just a couple
of classes meant to be imported into whatever script or service needs a
name generator (container names, test fixtures, world-building tools,
whatever).

The word lists themselves are the interesting part in practice, and they
come from all kinds of places: a file checked into the repo, a list
someone typed into a heredoc, or the output of another command piped in.
`WordBank.from_source` handles all three the same way.

## Install

Nothing to install yet beyond the standard library. Drop the `nameforge`
package on your path, or once this is packaged, `pip install nameforge`.

## Usage

Given two files:

```
# adjectives.txt
quiet
restless
brittle
```

```
# nouns.txt
river
hollow
foundry
```

```python
from nameforge import NameGenerator, WordBank

adjectives = WordBank.from_source("adjectives.txt")
nouns = WordBank.from_source("nouns.txt")

generator = NameGenerator("{adjective}-{noun}", adjective=adjectives, noun=nouns)

print(generator.generate())            # e.g. "brittle-foundry"
print(generator.generate_many(5))      # five more like it
```

### Reading from stdin

`WordBank.from_source` reads stdin when called with no argument (or with
`"-"`), so a word list can be piped in instead of read from disk:

```bash
cat nouns.txt | python -c "
from nameforge import WordBank
bank = WordBank.from_source()
print(len(bank))
"
```

This matters for anything that wants to build a word list on the fly with
shell tools (`grep`, `sort -R`, `head`) rather than maintaining a static
file.

### Reproducible output

Every generation method takes an optional `random.Random` instance, so
tests and anything else that needs deterministic output can pass a seeded
one instead of relying on the module-level default:

```python
import random

rng = random.Random(42)
generator.generate(rng)
```

## Word list format

Plain text, one word per line. Blank lines and lines starting with `#`
are ignored, so files can carry comments.

## Status

Early skeleton: template filling and file/stdin loading work. See the
roadmap for what's not built yet.

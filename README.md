# Metacritic game review visualisation

## How the data was acquired

### Adjectives
4800 adjectives were pulled from https://patternbasedwriting.com/elementary_writing_success/list-4800-adjectives/ using python's beautiful soup. Certain words were deemed to not be adjectives and thus manually removed.
#### Positive and negative
Positive and negative adjectives were taken from two sources (... and https://www.words-to-use.com/words/movies-tv/) then cross-referenced with the 4800 adjectives. Some adjectives were again manually removed.
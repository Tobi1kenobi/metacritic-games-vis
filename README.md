# Metacritic game review visualisation

## How the data was acquired

### Adjectives
4800 adjectives were pulled from https://patternbasedwriting.com/elementary_writing_success/list-4800-adjectives/ using python's beautiful soup. Certain words were deemed to not be adjectives and thus manually removed.
#### Positive and negative
Positive and negative adjectives were taken from two sources (... and https://www.words-to-use.com/words/movies-tv/) then cross-referenced with the 4800 adjectives. Some adjectives were again manually removed.

### Review text
Reviews were pulled from websites using the Beautifulsoup python package. It it possible that some text is derived from sources other than the body of the review e.g. user comments, but the hope is that this is by far the minority when looking at all the reviews' adjectives.

### Review scores, platforms and release dates
This data was pulled from https://www.kaggle.com/destring/metacritic-reviewed-games-since-2000

### Genres, developers and publisher
These will be pulled from the metacritic pages after generating a url using the games' names and platforms.


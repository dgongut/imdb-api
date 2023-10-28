import os

URL_IMDB_BASE = "https://www.imdb.com"
URL_SEARCH_IMDB = f'{URL_IMDB_BASE}/find/?s=tt&q='
URL_FILM_PAGE_IMDB = f'{URL_IMDB_BASE}/title/tt'
USER_AGENT = "Mozilla/5.0 (iPad; CPU OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
STATUS_CODE_OK = 200
STATUS_CODE_NOT_FOUND = 404
STATUS_CODE_ERROR = 502
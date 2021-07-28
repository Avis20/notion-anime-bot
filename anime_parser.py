
from urllib.parse import urlparse
from model import shikimori

ROUTE = {
    'shikimori.one': shikimori.parse
}


def search_data(url):
    parse_url = urlparse(url)
    result = ROUTE[parse_url.netloc](url)
    return result


if __name__ == '__main__':
    print(search_data("https://shikimori.one/animes/39247-kobayashi-san-chi-no-maid-dragon-s"))

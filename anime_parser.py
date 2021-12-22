
from urllib.parse import urlparse
from model import shikimori
from model import jutsu

ROUTE = {
    'shikimori.one': shikimori.parse,
    'jut.su': jutsu.parse
}


def search_data(url):
    parse_url = urlparse(url)
    result = ROUTE[parse_url.netloc](url)
    result['status'] = 'Разобрать'
    result['Category'] = 'Аниме'
    result['url'] = url
    result['Stoppet_at'] = 'S01E01'
    return result


if __name__ == '__main__':
    # print(search_data("https://shikimori.one/animes/39247-kobayashi-san-chi-no-maid-dragon-s"))
    print(search_data("https://shikimori.one/animes/43523-tsuki-ga-michibiku-isekai-douchuu"))
    # print(search_data("https://jut.su/bokurema/"))

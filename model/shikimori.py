import requests as r
from bs4 import BeautifulSoup


def parse(url):
    response = r.get(url, headers={
        'accept': "*/*",
        'User-Agent': 'Mozilla/5.0',
    })

    # TODO: pydantic
    result = dict()
    soup = BeautifulSoup(response.content, "html.parser")
    section = soup.find('section', {"class": "l-page"})
    # title
    header = section.find('header', {"class": 'head'})
    result['title'] = header.find('h1').text
    # cover
    content = section.find('div', {"class": "l-content"})
    image = content.find('div', {"class": "c-image"})
    result['cover'] = image.find('img')['src'].split('?')[0]

    return result


if __name__ == '__main__':
    print(parse("https://shikimori.one/animes/39247-kobayashi-san-chi-no-maid-dragon-s"))

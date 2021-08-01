import requests as r
from bs4 import BeautifulSoup
import re

def parse(url):

    response = r.get(url, headers={
        'accept': "*/*",
        'User-Agent': 'Mozilla/5.0',
    })

    # TODO: pydantic
    result = dict()
    soup = BeautifulSoup(response.content, "html.parser")
    # title
    header = soup.find('div', {"class": "watch_l"})
    text = header.find('h1').text
    for substr in ['Смотреть ', ' все серии']:
        text = text.replace(substr, '')
    result['title'] = text

    # cover
    style = header.find('div', {"class": "all_anime_title"})['style']
    print("style", style, 'type', type(style))
    match = re.search("http.*\.(jpg|png)", style)
    result['cover'] = match.group()


    return result


if __name__ == '__main__':
    print(parse("https://jut.su/bokurema/"))
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
    header = section.find('header', {"class": 'head'})
    result['title'] = header.find('h1').text
    return result


'''
Старый модуль для работы с notion
Основная проблема то что нельзя загружать файлы по api v1
пока заюзал сторонний модуль (https://pythonrepo.com/repo/jamalex-notion-py-python-third-party-apis-wrappers)
из неофициальных источников
'''

import requests
import utils
from requests.exceptions import HTTPError
import nlogger
import anime_parser

logger = nlogger.get_logger()
config = utils.get_config()
token = config.get('notion', 'token')
headers = {'Authorization': f"Bearer {token}"}


def _error(error_res):
    error_data = {'status': error_res.status_code, 'content': error_res.content}
    logger.error(f"Some error to send request! {error_data}")
    return None, error_data


def search(query):
    url = config.get('notion', 'api_host') + '/v1/search'
    data = {"query": query}
    response = None
    try:
        logger.debug(f"Try to send request = {url}")
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
    except HTTPError:
        return _error(response)
    else:
        logger.info("Success")
        return response.json(), None


def create_page(link):
    anime_data = anime_parser.search_data(link)
    # print(anime_data)
    url = config.get('notion', 'api_host') + '/v1/pages/'
    data = dict()
    data['parent'] = {'database_id': config.get('notion', 'database_id')}
    data['properties'] = {'Name': {'title': [{'text': {'content': anime_data.get('title')}}]}}
    try:
        logger.debug(f"Try to send request = {url}")
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
    except HTTPError as error:
        return _error(response)
    else:
        logger.info("Success")
        return response.json(), None

if __name__ == '__main__':
    # print(search('hello'))
    # create_page("https://shikimori.one/animes/39247-kobayashi-san-chi-no-maid-dragon-s")
    print(1)

import requests
import logging.config
import utils
from requests.exceptions import HTTPError

logging.config.fileConfig("logging.conf")
config = utils.get_config()
token = config.get('notion', 'token')
headers = {'Authorization': f"Bearer {token}"}


def _error(error_res):
    error_data = {'status': error_res.status_code, 'content': error_res.content}
    logging.error(f"Some error to send request! {error_data}")
    return None, error_data


def search(query):
    url = config.get('notion', 'api_host') + '/v1/search'
    data = {"query": query}
    try:
        logging.debug(f"Try to send request = {url}")
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
    except HTTPError as error:
        return _error(response)
    else:
        logging.info("Success")
        return response.json(), None


def create_page(title):
    url = config.get('notion', 'api_host') + '/v1/pages/'
    data = dict()
    data.update({'parent': {'database_id': "5a0601ec5c5a4c26b983561bd105b387"}})
    data.update({'properties': {'Name': {'title': [{'text': {'content': title}}]}}})
    try:
        logging.debug(f"Try to send request = {url}")
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
    except HTTPError as error:
        return _error(response)
    else:
        logging.info("Success")
        return response.json(), None


if __name__ == '__main__':
    # print(search('hello'))
    create_page('hello')

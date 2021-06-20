import requests
import logging.config
import utils
from requests.exceptions import HTTPError

logging.config.fileConfig("logging.conf")
config = utils.get_config()
token = config.get('notion', 'token')
headers = {'Authorization': f"Bearer {token}"}


def search(query):
    data = {"query": query}
    url = config.get('notion', 'host') + '/v1/search'
    try:
        logging.debug(f"Try to send request = {url}")
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
    except HTTPError as error:
        logging.error(f"Some error to send request! status={response.status_code}; content={response.content}")
    else:
        logging.info("Success")
        return response.json()


def create_page():
    pass


if __name__ == '__main__':
    print(search('hello'))

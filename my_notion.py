
from notion.client import NotionClient
import utils
from urllib.parse import urlparse, urljoin, urlencode, urlunparse

config = utils.get_config()
client = NotionClient(token_v2=config.get('notion', 'token_v2'))


def create_page(data):
    url_parse = list(urlparse(urljoin(config.get('notion', 'host'), config.get('notion', 'database_id'))))
    q_params = urlencode({'v': config.get('notion', 'v_param')})
    url_parse[4] = q_params
    cv = client.get_collection_view(urlunparse(url_parse))
    row = cv.collection.add_row()
    row.name = data.get('title')
    row.status = data.get('status')
    row.image = data.get('cover', '')
    return row, None


if __name__ == '__main__':
    create_page({'title': 'hello', 'status': 'Разобрать'})

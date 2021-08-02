from notion.client import NotionClient
import utils
from urllib.parse import urlparse, urljoin, urlencode, urlunparse

config = utils.get_config()
client = NotionClient(token_v2=config.get('notion', 'token_v2'))


def search_page(search_string):
    cv = collection_view()
    # result = {"results": None}
    result = list()
    for row in cv.collection.get_rows(search=search_string):
        result.append({
            "id": row.id,
            "title": row.name,
            "categories": row.category
        })
    return {"results": result}, None

def create_page(data):
    cv = collection_view()
    row = cv.collection.add_row()
    # for key in ['title', 'status', 'cover']:
    #     row.key = data.get(key, '')

    row.image = data.get('cover', '')
    row.title = data.get('title', '')
    row.status = data.get('status', '')
    row.Category = data.get('Category', '')
    row.url = data.get('url', '')
    row.Stoppet_at = data.get('Stoppet_at', '')

    return row, None


def collection_view():
    url_parse = list(urlparse(urljoin(config.get('notion', 'host'), config.get('notion', 'database_id'))))
    q_params = urlencode({'v': config.get('notion', 'v_param')})
    url_parse[4] = q_params
    return client.get_collection_view(urlunparse(url_parse))


if __name__ == '__main__':
    res = search_page('king')
    print('<b>Категория:</b>', res[1].get('categories', {}), '\n')
    # create_page({'title': 'hello', 'status': 'Разобрать'})

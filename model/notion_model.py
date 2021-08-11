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

    row.image = data.get('cover', '')

    print("before get_all_properties", row.get_all_properties())

    for key in ['title', 'status', 'Category', 'url', 'stopped_at']:
        row.set_property(key, data.get(key, ''))

    print("after get_all_properties", row.get_all_properties())

    return row, None


def collection_view():
    url_parse = list(urlparse(urljoin(config.get('notion', 'host'), config.get('notion', 'database_id'))))
    q_params = urlencode({'v': config.get('notion', 'v_param')})
    url_parse[4] = q_params
    return client.get_collection_view(urlunparse(url_parse))


if __name__ == '__main__':
    # res = search_page('king')
    # print('<b>Категория:</b>', res[1].get('categories', {}), '\n')
    create_page({'title': 'hello', 'status': 'Not started'})

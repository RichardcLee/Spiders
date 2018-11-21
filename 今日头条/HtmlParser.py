import json
from collections import namedtuple


class HtmlParser(object):
    def __init__(self):
        pass

    def _parse_html(self):
        pass

    def _parse_json(self, response):
        dataTuple = namedtuple('dataTuple', ['title', 'author', 'plays', 'url'])
        json_data = json.loads(response.text)
        dataSet = json_data.get('data')
        if dataSet:
            for data in dataSet:
                yield dataTuple(data.get('title'), data.get('media_name'), data.get('play_effective_count'),
                                data.get('source_url').replace('/group/', 'http://www.365yg.com/a'))
        else:
            print('can\'t get data!')

    def _parse_xml(self):
        pass

    def parse(self, response, type='json'):
        if type == 'html':
            return self._parse_html()
        elif type == 'json':
            return self._parse_json(response)
        elif type == 'xml':
            return self._parse_xml()
        else:
            pass

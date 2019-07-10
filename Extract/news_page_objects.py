import bs4
import requests
from common import config

class NewsPage:
	def __init__(self, news_site_uid, url):
		self._config = config()['news_sites'][news_site_uid]
		self._queries = self._config['queries']
		self._html = None
		self._url = url
		self._visit(self._url)

	def _select(self, query_string):
		return self._html.select(query_string)

	def _visit(self, url):
		response = requests.get(url)
		response.raise_for_status()
		self._html = bs4.BeautifulSoup(response.text, 'html.parser')




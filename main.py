import logging
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
news_sites_uids = ['washingtonpost', 'elcolombiano', 'eltiempo', 'elespectador']

def _extract():
	logger.info('Starting extract process')
	for news_site_uid in news_sites_uids:
		subprocess.run(['python', 'main.py', news_site_uid], cwd='./Extract')


if __name__ == '__main__':
	_extract()

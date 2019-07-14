import logging
import subprocess
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

news_sites_uids = ['washingtonpost', 'elcolombiano', 'eltiempo', 'elespectador']

def _extract():
	logger.info('Starting extract process')
	for news_site_uid in news_sites_uids:
		subprocess.run(['python', 'main.py', news_site_uid], cwd='./Extract')


def _transform():
	logger.info('Starting transform process')
	now = datetime.datetime.now().strftime('%Y_%m_%d')
	for news_site_uid in news_sites_uids:
		dirty_data_filename = '{}_{}_articles.csv'.format(news_site_uid, now)
		clean_data_filename = 'tidy_{}'.format(dirty_data_filename)
		subprocess.run(['python', 'main.py', dirty_data_filename], cwd='./Transform')


def main():
	_extract()
	_transform()


if __name__ == '__main__':
	main()
